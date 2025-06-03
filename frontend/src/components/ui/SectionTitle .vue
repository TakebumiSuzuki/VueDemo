<script setup>
    import { defineProps } from 'vue';

    const props = defineProps({
        text: {
            type: String,
            required: true,
        }
    });
</script>


<template>
    <h2 class="text-5xl font-medium py-13 text-center text-zinc-800 dark:text-zinc-100 tracking-wider">
        {{ text }}
    </h2>
</template>