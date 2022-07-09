<script>
    import {onMount} from "svelte";

    let closest = [];
    let expiring = [];

    onMount(async () => {
        const closestRes = await fetch("http://192.46.228.205:8000/item/list?sort=distance&user_id=[user_id]")
        closest = await closestRes.json()

        const expiringRes = await fetch("http://192.46.228.205:8000/item/list?sort=expiry&user_id=[user_id]")
        expiring = await expiringRes.json()
    })
</script>

<main class="bg-amber-50 min-h-screen p-2 pt-6 flex flex-col gap-6">
    <h1 class="font-bold text-5xl text-center mb-4 sm:text-left sm:pl-6">Market</h1>
    <section>
        <h2 class="font-medium text-2xl text-center sm:text-left sm:pl-6">Closest to you</h2>
        {#if closest.length === 0}
            <article class="m-4 p-6 bg-gray-200 rounded-xl flex items-center gap-2 shadow-xl sm:w-[400px] sm:h-[300px]">
                <p class="font-medium text-xl">Oh... the market is empty.<br/>If you have anything to share, do create a listing <a href="/listing/create" class="text-blue-800">here</a>!</p>
            </article>
        {/if}
    </section>
    <section>
        <h2 class="font-medium text-2xl text-center sm:text-left sm:pl-6">Expiring soon</h2>
        {#if expiring.length === 0}
            <article class="m-4 p-6 bg-gray-200 rounded-xl flex items-center gap-2 shadow-xl sm:w-[400px] sm:h-[300px] ">
                <p class="font-medium text-xl">Oh... the market is empty.<br/>If you have anything to share, do create a listing <a href="/listing/create" class="text-blue-800">here</a>!</p>
            </article>
        {/if}
    </section>
</main>
