/**
 * File size utility functions
 */

export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
};

export const getCompressionRatio = (originalSize, storedSize) => {
  if (!originalSize || !storedSize || originalSize === 0) {
    return null;
  }
  const ratio = ((originalSize - storedSize) / originalSize * 100);
  return Math.round(ratio);
};

export const getCompressionSavings = (originalSize, storedSize) => {
  if (!originalSize || !storedSize) {
    return null;
  }
  return originalSize - storedSize;
};

export const formatCompressionInfo = (originalSize, storedSize) => {
  const ratio = getCompressionRatio(originalSize, storedSize);
  const savings = getCompressionSavings(originalSize, storedSize);
  
  if (!ratio || !savings) {
    return null;
  }
  
  return {
    ratio,
    savings: formatFileSize(savings),
    original: formatFileSize(originalSize),
    stored: formatFileSize(storedSize)
  };
};
