<script setup>
    import { ref, reactive, watch, onBeforeUnmount } from 'vue';
    import { useRouter } from 'vue-router';
    import { useNotificationStore } from '@/stores/notification';
    import axios from 'axios';

    const router = useRouter(); // 任意: 登録後のリダイレクト用
    const notificationStore = useNotificationStore();
    import PictureIcon from '@/components/ui/PictureIcon.vue';
    import Button from '@/components/ui/Button.vue';

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
    const isProcessing = ref(false);
    const successMessage = ref('');
    const errorMessage = ref('');
    const validationErrors = reactive({}); // クライアントサイドのバリデーションエラー

    // ウォッチャーを設定
    watch(() => form.name, (newName, oldName) => {
        // 名前が変更されたら、名前に関するバリデーションエラーをクリア
        if (validationErrors.name) {
            validationErrors.name = ''; // または delete validationErrors.name;
        }
    });

    watch(() => form.category, (newCategory, oldCategory) => {
        // カテゴリが変更されたら、カテゴリに関するバリデーションエラーをクリア
        if (validationErrors.category) {
            validationErrors.category = '';
        }
    });

    watch(() => form.price, (newPrice, oldPrice) => {
        // 価格が変更されたら、価格に関するバリデーションエラーをクリア
        if (validationErrors.price) {
            validationErrors.price = '';
        }
    });

    // descriptionはnullableなので、バリデーションエラーが必ず出るわけではないが、
    // もしdescriptionに特有のバリデーションエラーがあるなら追加
    watch(() => form.description, (newDescription, oldDescription) => {
        if (validationErrors.description) {
            validationErrors.description = '';
        }
    });

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
                validationErrors.image = '画像ファイルを選択してください。';
                imageFile.value = null;
                imagePreviewUrl.value = null;
                return;
            }
            if (file.size > 16 * 1024 * 1024) { // 16MB
                validationErrors.image = '画像ファイルは16MBを超えられません。';
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

            // Content-Type は FormData を使う場合、Axiosが自動で 'multipart/form-data' を設定してくれる
            const response = await axios.post('/api/admin/create-item', formData);

            successMessage.value = 'The product was successfully added!';
            notificationStore.setNotification(`The item was successfully added!`, 'success');
            console.log('登録成功:', response.data);

            // フォームをリセット
            resetForm();

            // 任意: 登録成功後、商品一覧ページなどにリダイレクト
            // setTimeout(() => {
            //   router.push('/api/admin/create-item'); // '/api/admin/create-item' は商品一覧ページのルートパス例
            // }, 1500);

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

    // フォームをリセットする関数
    const resetForm = () => {
        form.name = '';
        form.description = '';
        form.category = '';
        form.price = null;
        imageFile.value = null;
        imagePreviewUrl.value = null;
        Object.keys(validationErrors).forEach(key => delete validationErrors[key]);
    };

    const goHome = () => {
        router.push({ name: 'Home' });
    }

</script>



<template>
    <div class="bg-zinc-200 dark:bg-zinc-700 flex items-center justify-center px-4 md:py-12 px-8">
        <div class="max-w-3xl w-full space-y-12 bg-white dark:bg-zinc-800 pt-12 pb-16 px-10 shadow-xl text-zinc-800 dark:text-zinc-100 rounded">

            <h2 class="text-center text-3xl font-medium ">
                Add New Item
            </h2>

            <!-- formタグは単なる見た目の要素ではなく、セマンティクス、アクセシビリティ、ブラウザのデフォルト機能など、
            多くの重要な役割を担っています。@submit.preventを使用している場合でもformタグは維持することを強く推奨します。 -->
            <form class="space-y-8 " @submit.prevent="submitForm">
                <!-- 成功メッセージ -->
                <div
                    v-if="successMessage"
                    class="fixed bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded
                        bottom-20 -right-full duration-500 ease-in-out transition-all -translate-x-full opacity-80
                    "
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
                        <label for="image" class="block text-sm font-medium">Product Image</label>
                        <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                            <div class="space-y-1 text-center">

                                <PictureIcon />

                                <div class="flex text-sm">
                                    <label for="file-upload" class="cursor-pointer font-medium text-indigo-600 hover:text-indigo-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-indigo-500"
                                    >
                                        <span>Upload Image</span>
                                        <input
                                            id="file-upload"
                                            name="file-upload"
                                            type="file"
                                            class="sr-only"
                                            @change="handleImageChange"
                                            accept="image/*"
                                        />
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
                    <Button text="Save Item" loadingText="Processing" :isLoading="isProcessing"
                        class="bg-gradient-to-br from-indigo-500 to-indigo-700 opacity-90 hover:opacity-100"
                        @click="submitForm"
                    />
                    <Button text="Cancel" loadingText="Cancelling" :isLoading="isProcessing"
                        class="bg-gradient-to-br from-pink-500 to-pink-700 opacity-90 hover:opacity-100"
                        @click="goHome"
                    />
                </div>
            </form>
        </div>
    </div>
</template>


