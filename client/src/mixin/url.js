function serverUrl() {
  if (process.env.NODE_ENV === 'production') {
    return '';
  }
  return 'http://localhost:5000';
}

export default serverUrl;
