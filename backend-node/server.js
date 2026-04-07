const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

const PYTHON_API_BASE = process.env.PYTHON_URL || "http://python-ai:8000";

app.use(express.json());

/**
 * Route: Get Sales Forecast for an Outlet
 * URL Example: http://localhost:3000/sales-prediction/1001
 */
app.get('/sales-prediction/:id', async (req, res) => {
    const outletId = req.params.id;

    try {
        console.log(`[Express] Requesting forecast for Outlet ID: ${outletId}`);
        const pythonResponse = await axios.get(`${PYTHON_API_BASE}/predict/${outletId}`);

        if (pythonResponse.data.status === true) {
            return res.json({
                success: true,
                message: "Prediction received from Python AI",
                data: pythonResponse.data.data
            });
        } else {
            return res.status(400).json({
                success: false,
                message: pythonResponse.data.message || "Prediction failed"
            });
        }

    } catch (error) {
        console.error("[Express Error]:", error.message);
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({
                success: false,
                message: "Python AI Server is offline. Please start 'python3 predict.py!!'."
            });
        }

        res.status(500).json({
            success: false,
            message: "Internal Server Error while connecting to AI service",
            error: error.message
        });
    }
});

app.listen(PORT, () => {
    console.log(`✅ Express Server running at http://localhost:${PORT}`);
    console.log(`🔗 Test Link: http://localhost:${PORT}/sales-prediction/1001`);
});