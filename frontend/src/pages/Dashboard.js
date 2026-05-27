import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Card,
  CardContent,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { DatePicker } from '@mui/x-date-pickers';
import { api } from '../services/api';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [selectedCountry, setSelectedCountry] = useState('all');
  const [dateRange, setDateRange] = useState([null, null]);
  const [dashboardData, setDashboardData] = useState(null);
  const [skuPerformance, setSkuPerformance] = useState([]);
  const [channelPerformance, setChannelPerformance] = useState([]);
  const [countryComparison, setCountryComparison] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, [selectedCountry, dateRange]);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedCountry !== 'all') params.country = selectedCountry;
      if (dateRange[0] && dateRange[1]) {
        params.date_from = dateRange[0].toISOString().split('T')[0];
        params.date_to = dateRange[1].toISOString().split('T')[0];
      }

      const response = await api.get('/dashboard/unified_dashboard/', { params });
      setDashboardData(response.data);
      setSkuPerformance(response.data.sku_performance);
      setChannelPerformance(response.data.channel_performance);
      setCountryComparison(response.data.country_comparison);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Regional Market Insights Dashboard
      </Typography>

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Country</InputLabel>
              <Select
                value={selectedCountry}
                onChange={(e) => setSelectedCountry(e.target.value)}
                label="Country"
              >
                <MenuItem value="all">All Countries</MenuItem>
                <MenuItem value="KE">Kenya</MenuItem>
                <MenuItem value="UG">Uganda</MenuItem>
                <MenuItem value="RW">Rwanda</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <DatePicker
              label="Start Date"
              value={dateRange[0]}
              onChange={(date) => setDateRange([date, dateRange[1]])}
              sx={{ width: '100%' }}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <DatePicker
              label="End Date"
              value={dateRange[1]}
              onChange={(date) => setDateRange([dateRange[0], date])}
              sx={{ width: '100%' }}
            />
          </Grid>
        </Grid>
      </Paper>

      {/* KPI Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Revenue
              </Typography>
              <Typography variant="h4">
                ${dashboardData?.total_revenue?.toLocaleString() || '0'}
              </Typography>
              <Chip
                label="+12.5% vs last month"
                color="success"
                size="small"
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Units Sold
              </Typography>
              <Typography variant="h4">
                {dashboardData?.total_quantity?.toLocaleString() || '0'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Active SKUs
              </Typography>
              <Typography variant="h4">{skuPerformance.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Avg. Price per Unit
              </Typography>
              <Typography variant="h4">
                $
                {(
                  skuPerformance.reduce((acc, sku) => acc + parseFloat(sku.avg_price || 0), 0) /
                  skuPerformance.length || 0
                ).toFixed(2)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              SKU Performance - Top 10 by Revenue
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
                data={skuPerformance.slice(0, 10)}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="sku__sku_code" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_revenue" fill="#8884d8" name="Revenue ($)" />
                <Bar dataKey="total_quantity" fill="#82ca9d" name="Quantity" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Channel Performance
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={channelPerformance}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={(entry) => `${entry.channel__name}: ${((entry.total_revenue / dashboardData?.total_revenue) * 100).toFixed(1)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="total_revenue"
                >
                  {channelPerformance.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Country Comparison
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
                data={countryComparison}
                margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="country__name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_revenue" fill="#8884d8" name="Revenue ($)" />
                <Bar dataKey="total_quantity" fill="#82ca9d" name="Quantity" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}