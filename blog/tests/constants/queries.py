popular_posts_query = """
    query {
     posts :popularPosts {
        edges {
          node {
            id
            author {
              fullName
              profile {
                image
              }
            }
            title
            abstract
            views
            likes
            readLength
            coverPhoto
            dateAdded
          }
        }
      }
    }
"""
