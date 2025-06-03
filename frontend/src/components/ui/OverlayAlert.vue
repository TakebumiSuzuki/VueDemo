<script setup>
    import { ref, onMounted } from 'vue'

    const props = defineProps({
        text: String,
        proceedButtonText: String,
        cancelButtonText: String,
    });

    // transitionタグは入れ子にするとうまくいかなかったので、このようにonMountedを使ったらうまくいった
    const showDialog = ref(false);
    onMounted(() =>{
        showDialog.value = true
    });

    const emit = defineEmits(['cancel', 'proceed']);

    const emitProceed = () => {
        emit('proceed')
    };
    const emitCancel = () => {
        emit('cancel')
    };
    // バックドロップクリック時の処理（子要素のクリックでは発火しないように）
    const handleBackdropClick = (event) => {
        if (event.target === event.currentTarget) {
            emit('cancel')
        }
    };


</script>


<template>

    <div class="fixed inset-0 bg-black/80 flex justify-center items-center z-100"
        @click="handleBackdropClick"
    >
        <transition
            enter-active-class="transition-all duration-500"
            enter-from-class="opacity-0 translate-y-full"
            enter-to-class="opacity-100 translate-y-0"
            leave-active-class="transition-all duration-500"
            leave-from-class="opacity-100 translate-y-0"
            leave-to-class="opacity-0 translate-y-full"
        >
            <div v-show="showDialog" class="w-[80%] md:w-1/2 bg-zinc-100/80 dark:bg-zinc-500/80 text-zinc-800 dark:text-zinc-100 px-6 py-8 rounded-lg flex flex-col justify-between">
                <p class="text-center ">{{text}}</p>

                <div class="flex md:flex-row-reverse flex-col justify-center items-center gap-4 md:gap-10 mt-8
                        [&>button]:px-4 [&>button]:py-2 [&>button]:rounded [&>button]:text-zinc-100
                        [&>button]:block [&>button]:md:w-1/2 [&>button]:w-full [&>button]:hover:cursor-pointer
                        [&>button]:transition [&>button]:duration-200 [&>button]:ease-in-out
                "
                >
                    <button type="button" @click="emitProceed"
                        class="bg-gradient-to-br from-pink-500 to-pink-700
                            hover:from-pink-600 hover:to-pink-800 opacity-80"
                    >
                        {{proceedButtonText}}
                    </button>
                    <button type="button" @click="emitCancel"
                        class="bg-gradient-to-br from-indigo-500 to-indigo-700
                            hover:from-indigo-600 hover:to-indigo-800 opacity-80"
                    >
                        {{cancelButtonText}}
                    </button>
                </div>
            </div>
        </transition>
    </div>

</template>
