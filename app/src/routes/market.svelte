<script>
    import {onMount} from "svelte";
    import Minimized from "$lib/Minimized.svelte";


    let closest = [];
    let currentClosest = 2;
    let expiring = [];
    let currentExpiring = 2;

    onMount(async () => {
        const closestRes = await fetch(`http://192.46.228.205:8000/item/list?sort=distance&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2luamkiLCJleHAiOjE2NTc1MTA2NTh9.J494t1ZiMSGl-FqVCSLSZ6ckaDvqC3ASbOTISy566Oc`)
        closest = await closestRes.json()

        const expiringRes = await fetch(`http://192.46.228.205:8000/item/list?sort=expiry&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2luamkiLCJleHAiOjE2NTc1MTA2NTh9.J494t1ZiMSGl-FqVCSLSZ6ckaDvqC3ASbOTISy566Oc`)
        expiring = await expiringRes.json()
    })
</script>

<main class="bg-amber-50 min-h-screen p-2 pt-6 flex flex-col gap-6">
    <h1 class="font-bold text-5xl text-center mb-4 sm:text-left sm:pl-6">Market</h1>
    <section>
        <h2 class="font-medium text-2xl text-center sm:text-left sm:pl-6">Closest to you</h2>
        <div class="grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-4">
            {#if closest.length === 0}
                <article
                        class="m-4 p-6 bg-gray-200 rounded-xl flex items-center gap-2 shadow-xl sm:w-[400px] sm:h-[300px]">
                    <p class="font-medium text-xl">Oh... the market is empty.<br/>If you have anything to share, do
                        create a
                        listing <a href="/listing/create" class="text-blue-800">here</a>!</p>
                </article>
            {:else}
                {#each closest.slice(0, currentClosest) as item}
                    <a href={`/listing/62ca47994b75c2df51a6f7cc`}>
                        <Minimized title={item.item_name} imageSrc="images/500.png" description={item.item_name}
                                   address="{item.address}" expiry={item.expiry}/>
                    </a>
                {/each}
                {#if currentClosest < closest.length}
                    <button
                            on:click={() => currentClosest = currentClosest + 2}
                            id="loadmore2"
                            type="button"
                            class="btn btn-secondary">
                        Show more
                    </button>
                {/if}
            {/if}
        </div>
    </section>
    <section>
        <h2 class="font-medium text-2xl text-center sm:text-left sm:pl-6">Expiring soon</h2>
        <div class="grid grid-cols-1 lg:grid-cols-3 xl:grid-cols-4">
            {#if expiring.length === 0}
                <article
                        class="m-4 p-6 bg-gray-200 rounded-xl flex items-center gap-2 shadow-xl sm:w-[400px] sm:h-[300px] ">
                    <p class="font-medium text-xl">Oh... the market is empty.<br/>If you have anything to share, do
                        create a
                        listing <a href="/listing/create" class="text-blue-800">here</a>!</p>
                </article>
            {:else}
                {#each expiring.slice(0, currentExpiring) as item}
                    <a href={`/listing/62ca47994b75c2df51a6f7cc`}>
                        <Minimized title={item.item_name} imageSrc="images/500.png" description={item.item_name}
                                   address="{item.address}" expiry={item.expiry}/>
                    </a>
                {/each}
                {#if currentExpiring < expiring.length}
                    <button
                            on:click={() => currentExpiring = currentExpiring + 2}
                            id="loadmore"
                            type="button"
                            class="btn btn-secondary">
                        Show more
                    </button>
                {/if}
            {/if}

        </div>
    </section>
</main>
