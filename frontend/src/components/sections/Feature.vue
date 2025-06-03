<script setup>
    import { ref, onMounted, onUnmounted, watch, onUpdated } from 'vue'
    import axios from 'axios'
    import debounce from 'lodash.debounce'

    const products = ref(null)
    const isLoading = ref(false)
    const error = ref(null)
    const searchQuery = ref('')

    let observer = null

    // 「再描画後にObserverを登録する」ためのフラグ
    const needsObserve = ref(false)

    // コンテナー要素（全ての .fade-in-element をまとめて querySelectorAll するため）
    const containerRef = ref(null)

    // products が変更されたら、再描画後にObserver登録するフラグを立てる
    watch(products, (newList) => {
        if (newList && observer) {
            needsObserve.value = true
        }
    })

    onMounted(async () => {
        isLoading.value = true
        error.value = null

        // IntersectionObserver の初期化
        observer = new IntersectionObserver(
            // 一つ目の引数は監視対象の要素がルート要素と交差したとき、または交差が解除されたときに実行される
            // コールバック関数で、IntersectionObserverEntry オブジェクトの配列（entries）と、
            // オブザーバーインスタンス自身（observer）が引数として渡されます。
            (entries) => {
                entries.forEach((entry) => {
                    // ここは交差に入ったとき。else節をこの後に書くと、交差から外れた場合になる。
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible')
                        observer.unobserve(entry.target)
                    }
                })
            },
            // 0.1は10%交差したら、コールバックが実行される
            { threshold: 0.1 }
        )
        await fetchAll()
    })

    async function fetchAll(){
        try {
            const response = await axios.get('/api/items')
            products.value = response.data
            // products を更新したので、レンダリング後に.observe() を呼ぶためにフラグを立てる
            needsObserve.value = true
        } catch (err) {
            console.error('データの取得に失敗しました:', err)
            error.value = 'Failed to load products data.'
        } finally {
            isLoading.value = false
        }
    }


    // DOM更新が終わった直後に呼ばれる。ここでフェードイン要素を一括登録する
    onUpdated(() => {
        if (!needsObserve.value || !observer || !containerRef.value) {
            return
        }

        // 古い監視が残っていたら一度クリアしておく
        observer.disconnect()

        // 新しく IntersectionObserver を再生成してもよいが、
        // ここでは同じインスタンスを利用しつつ、既存のコールバックだけ利用する。
        // （disconnect()後に再度同じobserverを使う場合、再observeが可能）

        // containerRef 内の .fade-in-element を全取得
        const elements = Array.from(
            containerRef.value.querySelectorAll('.fade-in-element')
        )

        // 一度「visible」クラスを消しておく（再度リストが入れ替わる可能性があるため）
        elements.forEach((el) => {
            el.classList.remove('visible')
        })

        // 取得したすべての要素をObserverに登録
        elements.forEach((el) => {
            observer.observe(el)
        })

        needsObserve.value = false
    })

    onUnmounted(() => {
        if (observer) {
            observer.disconnect()
            observer = null
        }
    })

    const fetchItems = debounce(async (query) => {
    if (query.length >= 2) {
        isLoading.value = true

        try {
        const response = await axios.get('/api/items/search', {
            params: { q: query }
        })
        products.value = response.data
        } catch (error) {
        console.error('Search error:', error)
        } finally {
        isLoading.value = false
        }
    } else if (query.length === 0) {
        // queryが空のときは全件取得
        await fetchAll()
    }
    }, 500)

    watch(searchQuery, (newQuery) => {
        fetchItems(newQuery)
    })

</script>


<template>
        <div class="px-4 md:px-12 pb-7 -mt-4">
            <input
                type="text"
                v-model="searchQuery"
                placeholder="Search Itmes"
                class="text-zinc-800/80 dark:text-zinc-100/80 border py-1 px-3 rounded block w-full md:max-w-[35%] ml-auto placeholder:italic tracking-wide"
            />
        </div>

    <!-- products が存在するときだけ描画する -->
    <div
        v-if="products && products.length"
        ref="containerRef"
        class="grid gap-7 grid-cols-1 md:grid-cols-3 max-w-[1200px] px-4 md:px-12 mx-auto mb-16"
    >
        <div
        v-for="product in products"
        :key="product.id"
        class="shadow-xl hover:cursor-pointer hover:scale-102 hover:opacity-80 transition-all duration-150 ease-in-out hover:shadow-2xl fade-in-element"
        >
        <RouterLink :to="{ name: 'Product', params: { productId: product.id } }">
            <div class="bg-white dark:bg-zinc-800 text-zinc-800 dark:text-zinc-100">
            <div class="relative">
                <img
                :src="product.image_url"
                :alt="product.name"
                class="w-full aspect-[16/10] object-cover object-center block"
                />
                <p
                class="bg-indigo-500/70 text-white text-xs px-1.5 py-1 size-fit rounded-xs leading-tight absolute top-2 right-2"
                >
                {{ product.category }}
                </p>
            </div>
            <div class="pt-2 pb-4 px-6">
                <p class="mt-1.5 text-lg">{{ product.name }}</p>
                <p class="text-base leading-tight mt-2">
                {{ product.description.length > 50
                    ? product.description.slice(0, 50) + '…'
                    : product.description }}
                </p>
                <p class="text-sm text-right mb-3 mt-6">
                {{ new Date(product.updated_at).toLocaleDateString('ja-JP', { year: 'numeric', month: '2-digit', day: '2-digit' }) }}
                </p>
            </div>
            </div>
        </RouterLink>
        </div>
    </div>

    <!-- ローディング中表示 -->
    <div v-else-if="isLoading" class="text-center py-12">
        読み込み中…
    </div>

    <!-- エラー表示 -->
    <div v-else-if="error" class="text-center text-red-500 py-12">
        {{ error }}
    </div>
</template>



<style scoped>
.fade-in-element {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
    will-change: opacity, transform;
}

/* こちらの方が詳細度が高いので優先される */
.fade-in-element.visible {
    opacity: 1;
    transform: translateY(0);
}
</style>


