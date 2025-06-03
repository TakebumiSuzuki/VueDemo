<script setup>
</script>

<template>
    <!--
        muted: ビデオの音声をミュート（消音）します。
        playsinline: iOSデバイスでビデオがフルスクリーンにならずに、ページ内でインライン再生されるようにします。
        ヒーロービデオでは通常この属性も指定します。
    -->
    <video autoplay loop muted playsinline
        class="w-full max-sm:h-[100vh] object-cover"
    >
        <source  src="@/assets/video.mp4" type="video/mp4">
    </video>

</template>