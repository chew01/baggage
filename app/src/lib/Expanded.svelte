<script>
    export let title
    export let description
    export let imageSrc
    export let address
    export let expiry
    import FaMapMarkedAlt from 'svelte-icons/fa/FaMapMarkedAlt.svelte'
    import FaCalendarTimes from 'svelte-icons/fa/FaCalendarTimes.svelte'

    export let accepted

    async function accept() {
        const res = await fetch("http://192.46.228.205:8000/item/listingAccept?item_id=62ca47994b75c2df51a6f7cc&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2luamkiLCJleHAiOjE2NTc1MTA2NTh9.J494t1ZiMSGl-FqVCSLSZ6ckaDvqC3ASbOTISy566Oc")

        const rres = await res.json()
        if (rres.status === true) {
            accepted = true
        }
    }

    async function remove() {
        const res = await fetch("http://192.46.228.205:8000/item/removeAccept?item_id=62ca47994b75c2df51a6f7cc&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2luamkiLCJleHAiOjE2NTc1MTA2NTh9.J494t1ZiMSGl-FqVCSLSZ6ckaDvqC3ASbOTISy566Oc")

        const rres = await res.json()
        if (rres.status === true) {
            accepted = false
        }
    }
</script>

<style>
    .icon {
        width: 24px;
        height: 24px;
    }
</style>

<article class="m-4 p-6 bg-gray-200 rounded-xl flex flex-col gap-2 shadow-xl sm:w-[400px] sm:h-[500px]">
    <h2 class="text-2xl font-bold">{title}</h2>
    <img src={imageSrc} alt="" class="my-2 rounded-lg shadow-xl max-h-72 max-w-72 object-cover"/>
    <p class="italic font-medium">{description}</p>
    <div class="flex gap-2">
        <div class="icon">
            <FaMapMarkedAlt/>
        </div>
        <p class="font-medium">{address}</p>
    </div>
    <div class="flex gap-2">
        <div class="icon">
            <FaCalendarTimes/>
        </div>
        <p class="font-medium">Expires on {expiry}</p>
    </div>
    {#if accepted === ""}
        <button on:click={accept} class="bg-white rounded-xl p-4 font-medium text-lg">Reserve deal</button>
    {:else}
        <button on:click={remove} class="bg-white rounded-xl p-4 font-medium text-lg">Remove reservation</button>
    {/if}
</article>
