<script setup>
    import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue';
    import { useMenuStore } from '@/stores/menu';
    import { useRoute } from 'vue-router';

    import logoUrl from '@/assets/images/logo.svg';
    import DarkToggle from '@/components/ui/DarkToggle.vue'
    import Hamburger from '@/components/ui/Hamburger.vue';

    const menuStore = useMenuStore();
    const headerRootElement = ref(null);

    const route = useRoute();
    const adminRouteNames  = ['EditProduct', 'CreateProduct'];
    // 現在の route.name が adminRouteNames に含まれていれば true
    const isAdminPage = computed(() => {
        return typeof route.name === 'string' && adminRouteNames.includes(route.name);
    });

    const updateOwnHeight = () => {
        if (headerRootElement.value) {
            const height = headerRootElement.value.offsetHeight;
            menuStore.headerHeight = height;
        }
    };

    onMounted(() => {
        nextTick(() => {
            updateOwnHeight();
        });
        window.addEventListener('resize', updateOwnHeight);
    });

    onUnmounted(() => {
        window.removeEventListener('resize', updateOwnHeight);
    });
</script>

<template>

    <div
        class="fixed top-0 left-0 right-0 z-10 flex flex-row justify-between items-center px-12 py-5  bg-white dark:bg-zinc-800 shadow-md"
        ref="headerRootElement"
    >
        <!-- ロゴ -->
        <router-link :to="{ name:'Home' }">
            <img :src="logoUrl" alt="Sneakers" class="cursor-pointer dark:invert hover:opacity-80 transition duration-150 ease-in-out">
        </router-link>


        <!-- ヘッダー右側 -->
        <div class="flex justify-center items-center gap-8">
            <div>
                <div v-if="isAdminPage" >
                    <router-link :to="{ name: 'Home' }" class="text-pink-600 border px-2 py-1 rounded-lg text-sm">
                        Admin Mode
                    </router-link>
                </div>

                <div v-else>
                    <router-link :to="{ name: 'CreateProduct' }">
                        <div class="text-zinc-800 dark:text-zinc-100 border rounded-lg px-2 py-1  text-sm min-w-24 text-center">
                            <span class="">Create Item</span>
                        </div>
                    </router-link>
                </div>
            </div>

            <DarkToggle/>

            <Hamburger/>

        </div>

    </div>
</template>