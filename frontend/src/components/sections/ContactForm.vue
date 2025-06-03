<script setup>
    import { ref } from 'vue';
    import axios from 'axios';
    import SuccessModal from '@/components/ui/SuccessModal.vue';

    const username = ref('');
    const email = ref('');
    const message = ref('');
    const showSuccessModal = ref(false);

    // 送信処理中の状態や結果メッセージ
    const isLoading = ref(false);
    const successMessage = ref('');
    const errorMessage = ref('');

    const sendMessage = async () => {
        showSuccessModal.value = false
        successMessage.value = ''; // 以前の成功メッセージをクリア
        errorMessage.value = '';

        if (!username.value || !email.value || !message.value) {
            errorMessage.value = 'すべての項目を入力してください。';
            return;
        }
        // メール形式の簡易チェック
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
            errorMessage.value = '有効なメールアドレスを入力してください。';
            return;
        }

        isLoading.value = true;
        const formData = {
            username: username.value,
            email: email.value,
            message: message.value,
        };

        try {
            const response = await axios.post('/api/message', formData);

            console.log('Success:', response.data);
            successMessage.value = 'メッセージが正常に送信されました！';
            // 送信成功後、フォームをクリア
            username.value = '';
            email.value = '';
            message.value = '';
            showSuccessModal.value = true

        } catch (error) {
            console.error('Error sending message:', error);
            if (error.response) {
                // サーバーからのエラーレスポンスがある場合
                errorMessage.value = `送信に失敗しました: ${error.response.data.message || error.message}`;
            } else if (error.request) {
                // リクエストは行われたがレスポンスがない場合
                errorMessage.value = '送信に失敗しました: サーバーから応答がありません。';
            } else {
                // その他のエラー
                errorMessage.value = `送信に失敗しました: ${error.message}`;
            }
        } finally {
            isLoading.value = false;
        }
    };

    // モーダルが閉じるイベントを受け取る関数
    const handleCloseModal = () => {
        showSuccessModal.value = false;
    };
</script>


<template>

    <SuccessModal
        :show="showSuccessModal"
        :message="successMessage"
        @close="handleCloseModal"
    />

    <div class="space-y-8 md:w-1/2 w-full">
        <div>
            <label for="username" class="block">Name:</label>
            <input type="text" id="username" v-model="username" class="px-2 py-1 w-full bg-white text-black" :disabled="isLoading">
        </div>
        <div>
            <label for="email" class="block">Email:</label>
            <input type="email" id="email" v-model="email" class="px-2 py-1 w-full bg-white text-black" :disabled="isLoading">
        </div>
        <div>
            <label for="message" class="block">Message:</label>
            <textarea id="message" v-model="message" class="px-2 py-1 w-full bg-white text-black" rows="5" :disabled="isLoading"></textarea>
        </div>

        <button
            class="px-18 py-3 border hover:cursor-pointer hover:bg-gray-600 transition duration-300 ease-in-out block mx-auto"
            type="button"
            @click="sendMessage"
            :disabled="isLoading"
        >
            {{ isLoading ? 'SENDING...' : 'SEND' }}
        </button>

        <!-- 送信結果メッセージ表示 -->
        <p v-if="errorMessage" class="text-red-500 mt-4">{{ errorMessage }}</p>
    </div>

</template>