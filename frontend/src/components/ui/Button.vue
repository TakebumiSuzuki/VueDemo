<script setup>
// import { defineProps } from 'vue';
import Spinner from '@/components/ui/Spinner.vue';

const props = defineProps({
    isLoading: {
        type: Boolean,
        default: false,
    },
    // ボタンのtype属性を親から受け取れるようにする
    type: {
        type: String,
        default: 'button', // デフォルトは 'button' にする (submitでない場合が多い)
    },
    // ローディング中のテキスト（任意：スロットを使わない場合）
    loadingText: {
        type: String,
        default: 'Processing...',
    },
    // 通常時のテキスト（任意：スロットを使わない場合）
    text: {
        type: String,
        default: 'Submit',
    }
});

// 親コンポーネントにイベントを発火させる
const emit = defineEmits(['click']);

function handleClick() {
    // ローディング中でなければクリックイベントを発火
    if (!props.isLoading) {
        emit('click');
    }
}
</script>

<template>
    <button
        :type="type"
        :disabled="isLoading"
        class="relative flex justify-center items-center py-2 px-8 border border-transparent rounded-md shadow-md
            text-base font-medium text-white hover:cursor-pointer transiton duration-200 ease-in-out md:w-1/2 w-full
            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        :class="{ 'opacity-50 cursor-not-allowed': isLoading }"
        @click="handleClick"
    >
        <span v-if="isLoading" class="absolute left-0 inset-y-0 flex items-center pl-3">
            <slot name="spinner">
                <Spinner />
            </slot>
        </span>

        <!-- isLoading 中はloadingText、そうでなければデフォルトスロットの内容を表示 -->
        <span v-if="isLoading">{{ loadingText }}</span>
        <span v-else>{{ text }}</span>
    </button>
</template>