<script setup>
    import { ref, reactive, onMounted, onBeforeUnmount } from 'vue';
    import { useRouter, useRoute } from 'vue-router'; // 任意: 登録後のリダイレクト用
    import { useNotificationStore } from '@/stores/notification';

    import axios from 'axios';
    import PictureIcon from '@/components/ui/PictureIcon.vue';
    import Button from '@/components/ui/Button.vue';
    import Spinner from '@/components/ui/Spinner.vue';
    import OverlayAlert from '@/components/ui/OverlayAlert.vue';

    const router = useRouter(); // 任意: エディットのリダイレクト用
    const route = useRoute();
    const notificationStore = useNotificationStore();


    const productId = ref(null);
    const form = reactive({
        name: '',
        category: '',
        price: null,
        description: '',
    });

    // 画像ファイルとプレビューURL
    const imageFile = ref(null);
    const imagePreviewUrl = ref(null);

    // UIの状態管理
    const isLoading = ref(false);
    const isProcessing = ref(false)
    const successMessage = ref('');
    const errorMessage = ref('');
    const validationErrors = reactive({}); // クライアントサイドのバリデーションエラー
    const showDeleteConfirmation = ref(false)

    onMounted( async ()=> {
        // URLパスから商品IDを取得 (例: /item/:productId)。必ず型はStringsになる。そしてStringsのままでok.
        const id = route.params.productId;
        if (!id) {
            errorMessage.value = "Product ID was not found from the url.";
            return;
        }
        productId.value = id;

        isLoading.value = true;
        try {
            // responseはAxiosResponseオブジェクト型で、
            // response.dataは、AxiosによってすでにパースされたJSオブジェクトが入っている。
            const response = await axios.get(`/api/item/${productId.value}`);
            const dataObj = response.data;

            form.name = dataObj.name;
            form.category = dataObj.category;
            form.price = dataObj.price;
            form.description = dataObj.description;
            imagePreviewUrl.value = dataObj.image_url;

        } catch (err) {
            console.error("Failed to fetch product details:", err);
            errorMessage.value = "Failed to obtain the product data. Please try later again.";

        } finally {
            isLoading.value = false;
        }
    })

    onBeforeUnmount(() => {
        if (imagePreviewUrl.value) {
            URL.revokeObjectURL(imagePreviewUrl.value);
        }
    });

    // 画像ファイルが選択されたときのハンドラー
    const handleImageChange = (event) => {
        // event.target.files[0] から取得される file は、JavaScriptの File オブジェクトのインスタンスです。
        // この File オブジェクトは、ユーザーが <input type="file"> で選択したファイルに関する情報
        // （ファイル名、MIMEタイプ、サイズ、最終更新日時など）と、そのファイルの内容（バイナリデータ）への参照を持っています。
        // ファイルのバイナリデータ自体は、ブラウザのメモリ上にロードされるか、ファイルシステムへのポインタとして扱われます。
        const file = event.target.files[0];
        if (file) {
            // ファイルタイプとサイズのバリデーション (クライアントサイド)
            if (!file.type.startsWith('image/')) {
                validationErrors.image = 'Please select an image file.';
                imageFile.value = null;
                imagePreviewUrl.value = null;
                return;
            }
            if (file.size > 16 * 1024 * 1024) {
                validationErrors.image = 'The file size cannot exceed 16MB.';
                imageFile.value = null;
                imagePreviewUrl.value = null;
                return;
            }

            imageFile.value = file;

            // 画像プレビューURLを生成
            // URL.createObjectURL()メソッドは、Fileオブジェクトからブラウザ内部でのみ有効な一時的なURL（blob: URL）を生成。
            // このURLを<img>タグのsrc属性にセットすることで、ユーザーはサーバーへのアップロードを待たずに、
            // 選択した画像ファイルを即座にプレビューできる。
            imagePreviewUrl.value = URL.createObjectURL(file);
            delete validationErrors.image; // エラーメッセージをクリア
        } else {
            imageFile.value = null;
            imagePreviewUrl.value = null;
        }
    };

    // クライアントサイドのフォームバリデーション
    const validateForm = () => {
        let isValid = true;
        Object.keys(validationErrors).forEach(key => delete validationErrors[key]); // エラーをクリア

        if (!form.name.trim()) {
            validationErrors.name = 'Product name required.';
            isValid = false;
        }
        if (!form.category.trim()) {
            validationErrors.category = 'Category is required.';
            isValid = false;
        }
        if (form.price === null || form.price <= 0 || !Number.isInteger(form.price)) {
            validationErrors.price = 'Price should be a positive integer.';
            isValid = false;
        }
        // descriptionはnullableなので必須チェックは不要

        return isValid;
    };

    // フォーム送信ハンドラー
    const submitForm = async () => {
        // メッセージとエラーをリセット
        successMessage.value = '';
        errorMessage.value = '';

        // クライアントサイドのバリデーションを実行
        if (!validateForm()) {
            errorMessage.value = 'Input error. Please check out the form.';
            return;
        }

        isProcessing.value = true;
        try {
            // FormData オブジェクトを作成 (ファイルアップロードには必須)
            const formData = new FormData();
            formData.append('name', form.name);
            formData.append('category', form.category);
            formData.append('price', form.price);

            // description は optional なので、値がある場合のみ追加
            if (form.description) {
                formData.append('description', form.description);
            }

            // 画像ファイルが選択されていれば追加
            if (imageFile.value) {
                formData.append('image', imageFile.value); // 'image' はバックエンドでファイルを受け取る際のキー名
            }

            // AxiosでPOSTリクエストを送信
            // Content-Type は FormData を使う場合、Axiosが自動で 'multipart/form-data' を設定してくれる
            const response = await axios.patch(`/api/admin/item/${productId.value}/edit`, formData);

            successMessage.value = 'Item was successfully updated.';
            notificationStore.setNotification(`Item was successfully updated.`, 'success');
            console.log('登録成功:', response.data);


            // 任意: 登録成功後、商品一覧ページなどにリダイレクト
            setTimeout(() => {
                router.push({ name: 'Product', params: { productId: productId.value } });
            }, 1000);

        } catch (error) {
            console.error('商品登録エラー:', error);
            if (error.response) {
                // APIからのエラーレスポンスがある場合
                errorMessage.value = `商品登録に失敗しました: ${error.response.data.message || '不明なエラー'}`;
                // バックエンドからのバリデーションエラーを処理する場合
                if (error.response.data.errors) {
                    Object.assign(validationErrors, error.response.data.errors);
                }
            } else if (error.request) {
                // リクエストは送信されたが、レスポンスがなかった場合 (ネットワークエラーなど)
                errorMessage.value = 'ネットワークエラーが発生しました。インターネット接続を確認してください。';
                } else {
                // その他のエラー
                errorMessage.value = '予期せぬエラーが発生しました。';
            }

        } finally {
            isProcessing.value = false;
        }
    };

    const goProduct = () => {
        router.push({ name: 'Product', params: { productId: productId.value } });
    }


    const deleteProduct = async () => {
        try{
            const response = await axios.delete(`/api/admin/item/${productId.value}`);

            console.log('登録成功:', response.data);
            successMessage.value = 'Item was deleted.';
            notificationStore.setNotification(`The item was deleted.`, 'success');
            router.push({ name: 'Home' });

        }catch (err) {
            console.error("Failed to delete item:", err);
            errorMessage.value = 'Failed to delete the item.'
        }
    }


</script>



<template>
    <transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-300"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
    >
        <OverlayAlert
            v-if="showDeleteConfirmation"
            text="Are you sure to delete this item?"
            proceedButtonText="Delete"
            cancelButtonText="Cancel"
            @cancel="showDeleteConfirmation=false"
            @proceed="deleteProduct"
        />
    </transition>



    <div class="bg-zinc-200 dark:bg-zinc-700 flex items-center justify-center py-12 px-8">

        <div class="max-w-3xl w-full space-y-12 bg-white dark:bg-zinc-800 pt-12 pb-16 px-10 shadow-xl text-zinc-800 dark:text-zinc-100 rounded">

            <h2 class="text-center text-3xl font-medium ">
                Update Item
            </h2>

            <div v-if="isLoading" class="min-h-[40vh] flex justify-center">
                <Spinner class="animate-spin size-12 text-gray-400 " />
            </div>

            <form v-else class="space-y-8" @submit.prevent="submitForm">
                <!-- 成功メッセージ -->
                <div
                    v-if="successMessage"
                    class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative"
                    role="alert"
                >
                    <span class="block md:inline">{{ successMessage }}</span>
                </div>

                <!-- エラーメッセージ -->
                <div
                    v-if="errorMessage"
                    class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
                    role="alert"
                >
                    <span class="block md:inline">{{ errorMessage }}</span>
                </div>


                <div class="space-y-6">
                    <!-- 商品名 -->
                    <div>
                        <label for="name" class="sr-only">Product Name</label>
                        <input
                            id="name"
                            name="name"
                            type="text"
                            v-model="form.name"
                            required
                            class="appearance-none block w-full px-3 py-2 border border-gray-300
                            placeholder-gray-500 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 md:text-sm rounded"
                            placeholder="Product Name"
                        />
                        <p v-if="validationErrors.name" class="text-red-500 text-xs mt-1">{{ validationErrors.name }}</p>
                    </div>

                    <!-- カテゴリ -->
                    <div class="mt-4">
                        <label for="category" class="sr-only">Category</label>
                        <input
                            id="category"
                            name="category"
                            type="text"
                            v-model="form.category"
                            required
                            class="appearance-none block w-full px-3 py-2 border border-gray-300
                            placeholder-gray-500 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 md:text-sm rounded"
                            placeholder="Category"
                        />
                        <p v-if="validationErrors.category" class="text-red-500 text-xs mt-1">{{ validationErrors.category }}</p>
                    </div>

                    <!-- 価格 -->
                    <div class="mt-4">
                        <label for="price" class="sr-only">価格</label>
                        <input
                            id="price"
                            name="price"
                            type="number"
                            v-model.number="form.price"
                            required
                            min="1"
                            class="appearance-none block w-full px-3 py-2 border border-gray-300
                            placeholder-gray-500 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500  md:text-sm rounded"
                            placeholder="Price (USD)"
                        />
                        <p v-if="validationErrors.price" class="text-red-500 text-xs mt-1">{{ validationErrors.price }}</p>
                    </div>

                    <!-- 説明 -->
                    <div class="mt-4">
                        <label for="description" class="sr-only">Product Description</label>
                        <textarea
                            id="description"
                            name="description"
                            v-model="form.description"
                            rows="4"
                            class="appearance-none block w-full px-3 py-2 border border-gray-300
                            placeholder-gray-500 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 md:text-sm rounded"
                            placeholder="Product Description"
                        ></textarea>
                        <p v-if="validationErrors.description" class="text-red-500 text-xs mt-1">{{ validationErrors.description }}</p>
                    </div>

                    <!-- 画像ファイル選択 -->
                    <div class="mt-4">
                        <label for="image" class="block text-sm font-medium ">Product Image</label>
                        <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                            <div class="space-y-1 text-center">

                                <PictureIcon />

                                <div class="flex text-sm">
                                    <label for="file-upload" class="cursor-pointer font-medium text-indigo-500 hover:text-indigo-400 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500">
                                        <span>Upload Image</span>
                                        <input
                                            id="file-upload"
                                            name="file-upload"
                                            type="file"
                                            class="sr-only" @change="handleImageChange"
                                            accept="image/*" />
                                    </label>
                                    <p class="pl-1">or Drag & Drop</p>
                                </div>
                                <p class="text-xs text-gray-400">
                                    PNG, JPG, GIF (Max 16MB)
                                </p>
                            </div>
                        </div>
                        <p v-if="validationErrors.image" class="text-red-500 text-xs mt-1">{{ validationErrors.image }}</p>
                    </div>

                    <!-- 画像プレビュー -->
                    <div v-if="imagePreviewUrl" class="mt-4">
                        <label class="block text-sm font-medium">Image Preview:</label>
                        <img :src="imagePreviewUrl" alt="Image Preview" class="mt-2 max-h-64 object-cover rounded-md shadow-md block mx-auto" />
                    </div>
                </div>



                <div class="flex md:flex-row-reverse flex-col md:justify-center items-center md:gap-10 gap-4 pt-6">
                    <Button text="Save" loadingText="Processing" :isLoading="isProcessing"
                        class="bg-gradient-to-br from-green-500 to-green-700 opacity-90 hover:opacity-100"
                        type="submit"
                    />

                    <Button text="Delete" loadingText="Processing" :isLoading="isProcessing"
                        class="bg-gradient-to-br from-pink-500 to-pink-700 opacity-90 hover:opacity-100"
                        @click="showDeleteConfirmation = true" type="button"
                    />

                    <Button text="Go Back" loadingText="Cancelling" :isLoading="isProcessing"
                        class="bg-gradient-to-br from-indigo-500 to-indigo-700 opacity-90 hover:opacity-100"
                        @click="goProduct" type="button"
                    />
                </div>
            </form>
        </div>
    </div>
</template>


