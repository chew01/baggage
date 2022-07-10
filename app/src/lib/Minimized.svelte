<script>
    export let title
    export let description
    export let imageSrc
    export let address
    export let expiry
    import FaMapMarkedAlt from 'svelte-icons/fa/FaMapMarkedAlt.svelte'
    import FaCalendarTimes from 'svelte-icons/fa/FaCalendarTimes.svelte'
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
</article>
