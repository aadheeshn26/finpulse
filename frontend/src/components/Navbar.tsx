import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Badge,
} from '@mui/material';
import {
  TrendingUp,
  Notifications,
  Settings,
  GitHub,
} from '@mui/icons-material';
import { motion } from 'framer-motion';

const Navbar: React.FC = () => {
  return (
    <AppBar 
      position="sticky" 
      elevation={0}
      sx={{
        background: 'rgba(26, 26, 46, 0.8)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Box
              sx={{
                background: 'linear-gradient(45deg, #00d4ff, #ff6b6b)',
                borderRadius: '12px',
                padding: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <TrendingUp sx={{ color: 'white', fontSize: '28px' }} />
            </Box>
            <Box>
              <Typography
                variant="h5"
                sx={{
                  fontWeight: 700,
                  background: 'linear-gradient(45deg, #00d4ff, #ff6b6b)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                FinPulse
              </Typography>
              <Typography
                variant="caption"
                sx={{ color: 'text.secondary', fontSize: '10px' }}
              >
                Financial Sentiment Analysis
              </Typography>
            </Box>
          </Box>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <IconButton 
              sx={{ 
                color: 'text.secondary',
                '&:hover': { color: 'primary.main' },
                transition: 'color 0.3s ease'
              }}
            >
              <Badge badgeContent={3} color="secondary">
                <Notifications />
              </Badge>
            </IconButton>
            
            <IconButton 
              sx={{ 
                color: 'text.secondary',
                '&:hover': { color: 'primary.main' },
                transition: 'color 0.3s ease'
              }}
            >
              <Settings />
            </IconButton>
            
            <IconButton 
              href="https://github.com/aadheeshn26/finpulse"
              target="_blank"
              sx={{ 
                color: 'text.secondary',
                '&:hover': { color: 'primary.main' },
                transition: 'color 0.3s ease'
              }}
            >
              <GitHub />
            </IconButton>
            
            <Box
              sx={{
                ml: 2,
                px: 2,
                py: 0.5,
                borderRadius: '20px',
                background: 'linear-gradient(45deg, #00d4ff, #ff6b6b)',
                display: 'flex',
                alignItems: 'center',
                gap: 1,
              }}
            >
              <Box
                sx={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  backgroundColor: '#4ade80',
                  animation: 'pulse 2s infinite',
                  '@keyframes pulse': {
                    '0%, 100%': {
                      opacity: 1,
                    },
                    '50%': {
                      opacity: 0.5,
                    },
                  },
                }}
              />
              <Typography variant="caption" sx={{ color: 'white', fontWeight: 500 }}>
                Live
              </Typography>
            </Box>
          </Box>
        </motion.div>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
