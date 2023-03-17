$.ajax({
  url: '/fetchPosts',
  data: {startIndex: 0, numToReturn: 0},
  type: 'GET',
  success: function(data) {
    console.log(data)
  },
  error: function(error) {
  console.error(error);
  }
});
