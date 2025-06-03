<script setup>
import { useMenuStore } from '@/stores/menu';
const menuStore = useMenuStore();

</script>

<template>
    <div
        class="fixed z-15 top-0 -left-[300px] bottom-0 w-[300px] px-9 py-10
            bg-neutral-900 text-white opacity-0
            transition-all duration-500 ease-in-out"
        :class="{ 'left-0 opacity-100' : menuStore.showMenu }"
    >
        <nav class="flex flex-col justify-center items-start py-4
                    [&>a]:py-5 [&>a]:border-t-1 [&>a]:last:border-b-1 [&>a]:block [&>a]:w-full [&>a]:hover:cursor-pointer
        ">
            <a class="" @click="menuStore.showMenu=false" href="#pick-up">PICK UP</a>
            <a class="" @click="menuStore.showMenu=false" href="#feature">FEATURE</a>
            <a class="" @click="menuStore.showMenu=false" href="#contact">CONTACT</a>
        </nav>

        <nav class="flex flex-col justify-center items-start mt-6 py-4 text-sm
                    [&>a]:py-2 [&>a]:block [&>a]:w-full [&>a]:hover:cursor-pointer
        ">
            <a class="" @click="menuStore.showMenu=false" id="#pick-up">Twitter</a>
            <a class="" @click="menuStore.showMenu=false" id="#feature">facebook</a>
            <a class="" @click="menuStore.showMenu=false" id="#contact">instagram</a>
        </nav>



    </div>
</template>