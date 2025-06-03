import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useMenuStore = defineStore('menu', () => {
    const showMenu = ref(false);
    const headerHeight = ref(0)

    function toggleMenu() {
        showMenu.value = !showMenu.value; // ref の値にアクセス・変更するには .value を使う
    }

    return {
        showMenu,
        toggleMenu,
        headerHeight,
    };
});