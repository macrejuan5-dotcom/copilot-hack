<script lang="ts">
  import type { Airport } from '$lib';

  export let data;
  export let form;

  const airports: Airport[] = data.airports;
  const days = Array.from({ length: 7 }, (_, index) => ({
    name: new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(new Date(0, 0, index + 1)),
    value: index + 1
  }));
</script>

<h1>Flight Delay Predictor</h1>
<p>Select a day and arrival airport to estimate the likelihood of a flight being delayed by more than 15 minutes.</p>

<form method="POST" action="?/getDelay">
  <select name="airport">
    {#each airports as airport (airport.id)}
      <option value={airport.id}>{airport.name}</option>
    {/each}
  </select>

  <select name="day">
    {#each days as day (day.value)}
      <option value={day.value}>{day.name}</option>
    {/each}
  </select>

  <button type="submit">Find delay</button>
</form>

{#if form && form.result}
  <div>There is a {Math.round(form.result.delay * 100)}% chance of a delay. We are {Math.round(form.result.certainty * 100)}% sure.</div>
{/if}
