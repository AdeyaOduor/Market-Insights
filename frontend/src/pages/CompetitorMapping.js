import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Paper,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from 'recharts';
import { api } from '../services/api';

export default function CompetitorMapping() {
  const [loading, setLoading] = useState(true);
  const [selectedCountry, setSelectedCountry] = useState('KE');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [pricingData, setPricingData] = useState([]);
  const [competitors, setCompetitors] = useState([]);
  const [marketShare, setMarketShare] = useState([]);

  useEffect(() => {
    fetchCompetitorData();
  }, [selectedCountry, selectedCategory]);

  const fetchCompetitorData = async () => {
    setLoading(true);
    try {
      const params = { country: selectedCountry };
      if (selectedCategory) params.category = selectedCategory;

      const pricingResponse = await api.get('/dashboard/pricing_intelligence/', { params });
      setPricingData(pricingResponse.data);

      // Fetch competitors and market share
      const competitorsResponse = await api.get('/competitors/', { params });
      setCompetitors(competitorsResponse.data);

      // Prepare competitive radar data
      const radarData = competitorsResponse.data.map(comp => ({
        subject: comp.name,
        A: comp.market_share || 0,
        B: comp.price_position || 0,
        C: comp.product_range || 0,
        fullMark: 100,
      }));
      setMarketShare(radarData);
    } catch (error) {
      console.error('Error fetching competitor data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LinearProgress />;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Competitor Intelligence & Price Mapping
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} md={4}>
          <FormControl fullWidth>
            <InputLabel>Country</InputLabel>
            <Select
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
              label="Country"
            >
              <MenuItem value="KE">Kenya</MenuItem>
              <MenuItem value="UG">Uganda</MenuItem>
              <MenuItem value="RW">Rwanda</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={4}>
          <FormControl fullWidth>
            <InputLabel>Category</InputLabel>
            <Select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              label="Category"
            >
              <MenuItem value="">All Categories</MenuItem>
              {/* Add categories from API */}
            </Select>
          </FormControl>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Competitive Positioning Radar
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={marketShare}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis angle={30} domain={[0, 100]} />
                <Radar
                  name="Market Share"
                  dataKey="A"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.6}
                />
                <Radar
                  name="Price Position"
                  dataKey="B"
                  stroke="#82ca9d"
                  fill="#82ca9d"
                  fillOpacity={0.6}
                />
                <Tooltip />
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Price Benchmarking
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={pricingData.slice(0, 20)}>
                <XAxis dataKey="sku" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="our_price"
                  stroke="#8884d8"
                  name="Our Price"
                />
                <Line
                  type="monotone"
                  dataKey="avg_competitor_price"
                  stroke="#82ca9d"
                  name="Avg Competitor Price"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Detailed Competitor Analysis
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Competitor</TableCell>
                    <TableCell>Market Share</TableCell>
                    <TableCell>Avg Price</TableCell>
                    <TableCell>Product Range</TableCell>
                    <TableCell>Key Categories</TableCell>
                    <TableCell>Price Position</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {competitors.map((competitor) => (
                    <TableRow key={competitor.id}>
                      <TableCell>{competitor.name}</TableCell>
                      <TableCell>
                        <Chip
                          label={`${competitor.market_share}%`}
                          color={competitor.market_share > 20 ? 'primary' : 'default'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>${competitor.avg_price}</TableCell>
                      <TableCell>{competitor.product_count} SKUs</TableCell>
                      <TableCell>
                        {competitor.categories?.slice(0, 2).map(cat => (
                          <Chip key={cat} label={cat} size="small" sx={{ mr: 0.5 }} />
                        ))}
                      </TableCell>
                      <TableCell>
                        {competitor.price_position > 0 ? (
                          <Chip label="Premium" color="warning" size="small" />
                        ) : (
                          <Chip label="Value" color="info" size="small" />
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}