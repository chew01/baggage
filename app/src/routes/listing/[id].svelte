<script>
    import Expanded from "$lib/Expanded.svelte";

    async function fetchd() {
        const res = await fetch(`http://192.46.228.205:8000/item/list?sort=id&item_id=62ca47994b75c2df51a6f7cc&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiS2luamkiLCJleHAiOjE2NTc1MTA2NTh9.J494t1ZiMSGl-FqVCSLSZ6ckaDvqC3ASbOTISy566Oc`)
        return await res.json()
    }

    let prom = fetchd()

</script>

{#await prom}
    <p>Loading...</p>
{:then data}
    <Expanded title={data[0].item_name} description={data[0].item_name}
              address="{data[0].address}" expiry={data[0].expiry} accepted="{data[0].accepted}"/>
{/await}
