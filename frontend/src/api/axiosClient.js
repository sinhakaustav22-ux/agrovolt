import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

// ─── Crop ─────────────────────────────────────────────────────────────────
export const predictCropYield = (data) => api.post('/crop/predict', data)
export const getCropTypes     = ()     => api.get('/crop/crop-types')

// ─── Solar ────────────────────────────────────────────────────────────────
export const getSolarForecast = (data) => api.post('/solar/forecast', data)

// ─── Irrigation ───────────────────────────────────────────────────────────
export const getIrrigationRecommendation = (data) => api.post('/irrigation/recommend', data)

// ─── Weather ──────────────────────────────────────────────────────────────
export const getWeather = (lat, lon) => api.get(`/weather/${lat}/${lon}`)

// ─── Farms ────────────────────────────────────────────────────────────────
export const getFarms         = ()           => api.get('/farms/')
export const createFarm       = (data)       => api.post('/farms/', data)
export const getFarmPredictions = (farmId)   => api.get(`/farms/${farmId}/predictions`)

export default api
