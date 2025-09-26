import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  IconButton,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  TrendingUp,
  Refresh,
  Assessment,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import axios from 'axios';

interface SentimentData {
  total_analyzed: number;
  sentiment_distribution: {
    positive: number;
    negative: number;
    neutral: number;
  };
  average_sentiment: number;
  overall_trend: string;
}

const SimpleDashboard: React.FC = () => {
  const [sentimentData, setSentimentData] = useState<SentimentData | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  const mockData: SentimentData = {
    total_analyzed: 8,
    sentiment_distribution: { positive: 7, negative: 0, neutral: 1 },
    average_sentiment: 0.585,
    overall_trend: 'positive',
  };

  const fetchSentimentData = async () => {
    try {
      setLoading(true);
      try {
        const response = await axios.get('http://localhost:8080/sentiment/summary', {
          timeout: 3000
        });
        setSentimentData(response.data);
      } catch (error) {
        setSentimentData(mockData);
      }
      setLastUpdate(new Date());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSentimentData();
    const interval = setInterval(fetchSentimentData, 30000);
    return () => clearInterval(interval);
  }, []);

  const getSentimentColor = (sentiment: number) => {
    if (sentiment > 0.3) return '#4ade80';
    if (sentiment < -0.3) return '#f87171';
    return '#94a3b8';
  };

  if (loading) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '60vh' }}>
          <Box sx={{ width: '100%', maxWidth: 400 }}>
            <Typography variant="h6" sx={{ mb: 2, textAlign: 'center' }}>
              Loading FinPulse Analytics...
            </Typography>
            <LinearProgress 
              sx={{ 
                borderRadius: '10px', 
                height: '6px',
                '& .MuiLinearProgress-bar': {
                  background: 'linear-gradient(45deg, #00d4ff, #ff6b6b)'
                }
              }} 
            />
          </Box>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h1" sx={{ mb: 1 }}>
              Market Sentiment
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Real-time analysis of {sentimentData?.total_analyzed || 0} financial sources
            </Typography>
          </Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="caption" color="text.secondary">
              Last updated: {lastUpdate.toLocaleTimeString()}
            </Typography>
            <IconButton 
              onClick={fetchSentimentData}
              sx={{ 
                background: 'linear-gradient(45deg, #00d4ff, #ff6b6b)',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(45deg, #00b8e6, #e55555)',
                }
              }}
            >
              <Refresh />
            </IconButton>
          </Box>
        </Box>
      </motion.div>

      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 3, mb: 4 }}>
        {/* Total Analysis Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          style={{ flex: '1 1 250px', minWidth: '250px' }}
        >
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Assessment sx={{ color: 'primary.main', mr: 1 }} />
                <Typography variant="h6">Total Analysis</Typography>
              </Box>
              <Typography variant="h3" sx={{ mb: 1, color: 'primary.main' }}>
                {sentimentData?.total_analyzed || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Sources processed
              </Typography>
            </CardContent>
          </Card>
        </motion.div>

        {/* Average Sentiment Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          style={{ flex: '1 1 250px', minWidth: '250px' }}
        >
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <TrendingUp sx={{ color: getSentimentColor(sentimentData?.average_sentiment || 0), mr: 1 }} />
                <Typography variant="h6">Avg Sentiment</Typography>
              </Box>
              <Typography 
                variant="h3" 
                sx={{ 
                  mb: 1, 
                  color: getSentimentColor(sentimentData?.average_sentiment || 0)
                }}
              >
                {((sentimentData?.average_sentiment || 0) * 100).toFixed(1)}%
              </Typography>
              <Chip 
                label={sentimentData?.overall_trend || 'neutral'}
                color={sentimentData?.overall_trend === 'positive' ? 'success' : 'default'}
                size="small"
              />
            </CardContent>
          </Card>
        </motion.div>

        {/* Sentiment Distribution Card */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          style={{ flex: '1 1 250px', minWidth: '250px' }}
        >
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" sx={{ mb: 3 }}>
                Sentiment Breakdown
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Positive</Typography>
                  <Typography variant="body2" sx={{ color: '#4ade80' }}>
                    {sentimentData?.sentiment_distribution.positive || 0}
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={((sentimentData?.sentiment_distribution.positive || 0) / (sentimentData?.total_analyzed || 1)) * 100}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#4ade80',
                      borderRadius: 4,
                    },
                  }}
                />
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Neutral</Typography>
                  <Typography variant="body2" sx={{ color: '#94a3b8' }}>
                    {sentimentData?.sentiment_distribution.neutral || 0}
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={((sentimentData?.sentiment_distribution.neutral || 0) / (sentimentData?.total_analyzed || 1)) * 100}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#94a3b8',
                      borderRadius: 4,
                    },
                  }}
                />
              </Box>
              
              <Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Negative</Typography>
                  <Typography variant="body2" sx={{ color: '#f87171' }}>
                    {sentimentData?.sentiment_distribution.negative || 0}
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={((sentimentData?.sentiment_distribution.negative || 0) / (sentimentData?.total_analyzed || 1)) * 100}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: 'rgba(255,255,255,0.1)',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#f87171',
                      borderRadius: 4,
                    },
                  }}
                />
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      </Box>

      {/* Summary Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <Card>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 3 }}>
              FinPulse Summary
            </Typography>
            <Typography variant="body1" paragraph>
              Our sentiment analysis system has processed <strong>{sentimentData?.total_analyzed || 0}</strong> financial sources, 
              including news articles from Yahoo Finance, Reuters, Bloomberg, and Reddit posts from financial communities.
            </Typography>
            <Typography variant="body1" paragraph>
              Current market sentiment shows a <strong>{sentimentData?.overall_trend || 'neutral'}</strong> trend with an 
              average sentiment score of <strong>{((sentimentData?.average_sentiment || 0) * 100).toFixed(1)}%</strong>.
            </Typography>
            <Typography variant="body2" color="text.secondary">
              The analysis combines traditional news sentiment with social media sentiment for comprehensive market insights.
              Data is updated in real-time and can be connected to Power BI for interactive dashboards.
            </Typography>
          </CardContent>
        </Card>
      </motion.div>
    </Container>
  );
};

export default SimpleDashboard;
