import { Client, Environment } from "square";

const client = new Client({
  accessToken: process.env.SQUARE_ACCESS_TOKEN,
  environment: Environment.Production, // change to Sandbox if using sandbox token
});

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  try {
    const { amount = 500, currency = "USD", name = "SSRT" } = req.body || {};

    const idempotencyKey = crypto.randomUUID();

    const resp = await client.checkoutApi.createPaymentLink({
      idempotencyKey,
      quickPay: {
        name,
        priceMoney: { amount, currency },
        locationId: process.env.SQUARE_LOCATION_ID,
      },
    });

    const url = resp?.result?.paymentLink?.url;
    if (!url) return res.status(500).json({ error: "No payment link URL returned", resp });

    return res.status(200).json({ url });
  } catch (err) {
    return res.status(500).json({
      error: err?.message || "Square error",
      details: err?.errors || null,
    });
  }
}

