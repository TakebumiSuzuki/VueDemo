<script setup>
    const props = defineProps({
        show: { type: Boolean, default: false },
        message: { type: String, default: '操作が成功しました！'}
    });

    const emit = defineEmits(['close']);
    const closeModal = () => {
        emit('close');
    };
</script>

<template>

    <Transition name="modal-fade">
        <div v-if="show">
            <div
                class="fixed z-20 inset-0 bg-black/70 flex justify-center items-center"
                @click.self="closeModal"
                @keydown.esc="closeModal"
            >
                <div class="relative flex justify-center items-center w-100 h-40 bg-white/90 text-black rounded-lg">
                    {{ message }}
                    <button
                        class="absolute top-3 right-3 size-8 border p-1 text-gray-500 flex justify-center items-center rounded hover:cursor-pointer"
                        @click="closeModal"
                    >
                        X
                    </button>
                </div>
            </div>
        </div>
    </Transition>

</template>


<style>
    .modal-fade-enter-active,
    .modal-fade-leave-active {
        transition: opacity 0.3s;
    }
    .modal-fade-enter-from,
    .modal-fade-leave-to {
        opacity: 0;
    }
    .modal-fade-enter-to,
    .modal-fade-leave-from {
        opacity: 1;
    }
</style>