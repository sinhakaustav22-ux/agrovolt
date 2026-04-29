import { useEffect, useState } from 'react'
import StatCard from '../components/StatCard'
import WeatherCard from '../components/WeatherCard'
import { getWeather, getFarms } from '../api/axiosClient'
import useStore from '../store/useStore'
import { Link } from 'react-router-dom'

// Default coordinates: Bhubaneswar, India
const DEFAULT_LAT = 20.2961
const DEFAULT_LON = 85.8245

export default function Home() {
  const { weatherData, setWeatherData, farms, setFarms } = useStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchData() {
      try {
        const [weatherRes, farmsRes] = await Promise.all([
          getWeather(DEFAULT_LAT, DEFAULT_LON),
          getFarms()
        ])
        setWeatherData(weatherRes.data)
        setFarms(farmsRes.data)
      } catch (err) {
        console.error('Dashboard load error:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-green-600 text-xl font-semibold">
        Loading AgroVolt Dashboard...
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-green-800">🌱 AgroVolt Dashboard</h1>
          <p className="text-gray-500 mt-1">
            Smart Agrovoltaic Management — Solar + Crop + Irrigation in one place
          </p>
        </div>
        <Link to="/predict" className="btn-primary">
          + Run New Prediction
        </Link>
      </div>

      {/* Stats Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard icon="🌾" label="Total Farms"        value={farms.length}  unit="farms"    color="green"  />
        <StatCard icon="☀️" label="Avg Solar Output"   value="142"           unit="kWh/day"  color="yellow" />
        <StatCard icon="💧" label="Water Saved"        value="28"            unit="% less"   color="blue"   />
        <StatCard icon="📈" label="Land Equivalent"    value="1.42"          unit="LER"      color="green"  />
      </div>

      {/* Weather + Info */}
      <div className="grid md:grid-cols-2 gap-6">
        <WeatherCard data={weatherData} />

        <div className="card">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">🔬 What is Agrovoltaics?</h3>
          <p className="text-sm text-gray-600 leading-relaxed">
            Agrovoltaics places solar panels <strong>above crops</strong> on the same land.
            Panels create partial shade that reduces heat stress on crops, cuts irrigation needs
            by up to 30%, and simultaneously generates electricity. The <strong>Land Equivalent
            Ratio (LER)</strong> proves this dual-use approach is more efficient than keeping
            farming and solar separate.
          </p>
          <div className="mt-4 flex gap-3">
            <Link to="/predict"   className="btn-primary text-sm">Run Prediction →</Link>
            <Link to="/analytics" className="btn-secondary text-sm">View Analytics →</Link>
          </div>
        </div>
      </div>

      {/* Farms List */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold text-gray-700">🏡 Your Farms</h3>
          <Link to="/settings" className="text-green-600 text-sm hover:underline">
            + Add Farm
          </Link>
        </div>
        {farms.length === 0 ? (
          <p className="text-gray-400 text-sm">
            No farms yet. Go to Settings to add your first farm.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left border-b text-gray-500">
                  <th className="pb-2">Name</th>
                  <th className="pb-2">Location</th>
                  <th className="pb-2">Crop</th>
                  <th className="pb-2">Panels</th>
                  <th className="pb-2">Area (ha)</th>
                </tr>
              </thead>
              <tbody>
                {farms.map(farm => (
                  <tr key={farm.id} className="border-b last:border-0 hover:bg-green-50">
                    <td className="py-2 font-medium">{farm.name}</td>
                    <td className="py-2 text-gray-500">{farm.location}</td>
                    <td className="py-2">{farm.crop_type}</td>
                    <td className="py-2">{farm.panel_count}</td>
                    <td className="py-2">{farm.area_hectares}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
