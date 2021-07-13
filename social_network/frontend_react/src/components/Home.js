import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosApi";
import UserPost from "./UserPost";
import Container from "@material-ui/core/Container"
import CreatePost from "./CreatePost";
import InfiniteScroll from 'react-infinite-scroll-component';
import { makeStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import Divider from "@material-ui/core/Divider";


export default function Home() {

  const [posts, setPosts] = useState([]);
  const [nextPostsUrl, setNextPostsUrl] = useState(null);
  const [isNextPosts, setIsNextPosts] = useState(true);

  const useStyles = makeStyles((theme) => ({
    root: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      '& > * + *': {
        marginLeft: theme.spacing(2),

      },
    },
  }));

  // Passing an empty array as the second argument to useEffect 
  // makes it only run on mount and unmount, thus stopping any infinite loops.
  useEffect(() => {
    getNextPosts();
  }, []);


  const getNextPosts = async () => {

    try {

        let url = nextPostsUrl == null ? "next_posts/" : nextPostsUrl;

        console.log("url: " + url)

    // chnage to get next posts
    let response = await axiosInstance.get(url);

    let nextPosts = response.data.results.map((post) => ({
        postId: post.pk,
        userId: post.user_id,
        username: post.username,
        text: post.text,
        dateTime: post.date_time,
        likes: post.number_of_likes,
    }));

   
    // simulates loading time
    setTimeout(() => {

         // add new posts to current posts
        setPosts(posts.concat(nextPosts));
        setNextPostsUrl(response.data.next);
        setIsNextPosts(response.data.next == null ? false : true);

    }, 1500);

    } catch (error) {
        console.log(error.stack);
    }
  };

  const classes = useStyles();

 
    return (
      <div>

        <Box m={2} />
        
        <Container>
          <div>{ <CreatePost/> }</div>

        <Box m={5} />

        <Divider light className={classes.divider} />

        <Box m={3} />

        <Grid
            container
            direction="column"
            justify="centre"
            alignItems="center"
            spacing={1}
          >
          <Grid item xs={12}>
              <Typography variant="h4">
                <Box fontWeight="fontWeightBold"> All Posts </Box>
              </Typography>
            </Grid>
          </Grid>

          <Box m={2} />

          </Container>


        <InfiniteScroll
          dataLength={posts.length}
          next={getNextPosts}
          hasMore={isNextPosts}
          loader={
            <div className={classes.root}>
              {" "}
              <CircularProgress color="secondary" />{" "}
            </div>
          }
        >

          {posts.map((post) => (
            <div key={post.pk}>
              <Container>
                <UserPost
                  postId={post.postId}
                  userId={post.userId}
                  username={post.username}
                  text={post.text}
                  dateTime={post.dateTime}
                  likes={post.likes}
                />
              </Container>
            </div>
          ))}
        </InfiniteScroll>
      </div>
    );
  }
