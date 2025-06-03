<script setup>
import { useMenuStore } from '@/stores/menu';

const menuStore = useMenuStore();

function toggleMenuState() {
    menuStore.toggleMenu();
}

</script>

<template>
    <div
        class="size-8 relative z-100 hover:cursor-pointer
            [&_div]:absolute [&_div]:w-full [&_div]:h-[2px] [&_div]:top-1/2 [&_div]:left-0 [&_div]:bg-black dark:[&_div]:bg-zinc-100 [&_div]:rounded-md [&_div]:transition [&_div]:duration-500 [&_div]:ease-in-out "
        @click="toggleMenuState">

        <div class="-translate-y-[calc(50%+11px)]" :class="{ '-rotate-315 !-translate-y-[calc(50%+0px)] !bg-white' : menuStore.showMenu }"></div>
        <div class="-translate-y-[calc(50%+0px)]" :class="{ 'opacity-0 !bg-white' : menuStore.showMenu }"></div>
        <div class="-translate-y-[calc(50%-11px)]" :class="{ 'rotate-315 !-translate-y-[calc(50%+0px)] !bg-white' : menuStore.showMenu }"></div>
    </div>

    <div class="z-50 fixed inset-0 bg-black/70"
        v-if="menuStore.showMenu"
        @click="menuStore.showMenu = false"
    >
    </div>

</template>