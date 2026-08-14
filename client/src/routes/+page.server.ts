export async function load({ fetch }) {
  const res = await fetch('http://localhost:5000/airports');
  const airports = await res.json();
  return { airports };
}

export const actions = {
  getDelay: async ({ fetch, request }) => {
    const data = await request.formData();
    const day_of_week = data.get('day');
    const airport_id = data.get('airport');

    const res = await fetch(`http://localhost:5000/predict?day_of_week=${day_of_week}&airport_id=${airport_id}`);
    const result = await res.json();
    return { result };
  }
};
