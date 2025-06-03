import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useNotificationStore = defineStore('notification', () => {
    const message = ref(null);
    const type = ref(null);
    // setTimeout のIDを管理するための内部的なref
    const _timeoutId = ref(null);

    function setNotification(msg, typeParam, duration = 7000) {
        message.value = msg;
        type.value = typeParam;

        if (_timeoutId.value) {
            clearTimeout(_timeoutId.value); // 既存のタイマーがあればクリア
        }
        _timeoutId.value = setTimeout(() => {
            clearNotification();
        }, duration);
    }

    function clearNotification() {
        message.value = null;
        type.value = null;
        if (_timeoutId.value) {
            clearTimeout(_timeoutId.value);
            _timeoutId.value = null;
        }
    }

    // 3. 外部に公開する状態とアクションを return する
    return {
        message,         // message.value でアクセスできるようになる (テンプレート内では .value 不要)
        type,            // type.value でアクセスできるようになる (テンプレート内では .value 不要)
        setNotification,
        clearNotification,
    };
});