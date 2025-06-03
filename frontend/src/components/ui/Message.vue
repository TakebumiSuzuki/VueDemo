
<script setup>
    import { storeToRefs } from 'pinia';
    import { useNotificationStore } from '@/stores/notification';
    import XIcon from '@components/ui/XIcon.vue';
    const notificationStore = useNotificationStore();
    const { message, type } = storeToRefs(notificationStore);

</script>

<template>
    <div class="flex flex-row items-center justify-center gap-2">
        <p class="text-lg">{{ message }}</p>

        <button @click="notificationStore.clearNotification">
            <XIcon class="size-6 hover:cursor-pointer hover:scale-105"/>
        </button>
    </div>

</template>

<style scoped>
.success {
    color: green;
    background-color: #8dc28e; /* 緑 */
}
.error {
    color: red;
    background-color: #d78e89; /* 赤 */
}
.info {
    color: yellow;
    background-color: #81add1; /* 青 */
}
</style>