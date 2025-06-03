<script setup>
  import { ref } from 'vue';
  import ModalMenu from '@components/ui/ModalMenu.vue';
  import TheHeader from '@components/layout/TheHeader.vue';
  import TheMain from '@components/layout/TheMain.vue';
  import TheFooter from '@components/layout/TheFooter.vue';
  import Message from '@components/ui/Message.vue';


  // JavaScriptやTypeScriptのモジュールをインポートする際、拡張子を省略するのは一般的な慣習です。
  import { useMenuStore } from '@/stores/menu';
  const menuStore = useMenuStore();

  import { storeToRefs } from 'pinia';
  import { useNotificationStore } from '@/stores/notification';
  const notificationStore = useNotificationStore();
  const { message, type } = storeToRefs(notificationStore);
</script>


<template>

  <!-- 通知メッセージの表示 -->
  <transition
    enter-active-class="transition-all duration-1500 ease-linear"
    enter-from-class="translate-x-[400px]"
    enter-to-class="translate-x-0"
    leave-active-class="transition-all duration-2000 ease-linear"
    leave-from-class="!opacity-85"
    leave-to-class="!opacity-0"
  >
    <!-- opacityなどの様に同じクラスをtransitionにも入れる場合には!を使わないと競合する -->
    <Message v-if="message"
      class="fixed z-200 top-16 right-10 px-8 py-1 opacity-80 rounded"
      :class="[type]"/>
  </transition>


  <div class="flex flex-col min-h-screen bg-white dark:bg-zinc-700">
    <ModalMenu/>

    <header>
      <TheHeader/>
    </header>

    <!-- 実はヘッダー内に入れた方がよくない？ -->
    <div :style="`height: ${ menuStore.headerHeight }px`"></div>

    <main class="flex-grow">
      <TheMain>
        <router-view/>
      </TheMain>
    </main>

    <footer id="contact">
      <TheFooter/>
    </footer>

  </div>

</template>



<style scoped>

</style>
