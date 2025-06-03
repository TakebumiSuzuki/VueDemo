<script setup>
    import { ref, onBeforeMount } from 'vue';
    let darkMode = ref(false)
    let toggleDarkMode = () => {
        darkMode.value = !darkMode.value;

        // localStorage に新しいダークモードの状態を保存（文字列として）
        localStorage.setItem('darkMode', darkMode.value.toString());
        if (darkMode.value) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }

    onBeforeMount(()=>{
        if (typeof window.darkMode === 'boolean') {
            darkMode.value = window.darkMode;
        }
    })
</script>

<template>
    <div
        class="relative h-6 w-10 bg-gray-400 rounded-full "
        @click="toggleDarkMode"
    >
        <div
            class="size-5 rounded-full absolute top-0.5 left-0.5 bg-zinc-100 transition-all duration-300 ease-in-out"
            :class="darkMode ? 'translate-x-4':'translate-x-0'"

        ></div>

    </div>
</template>