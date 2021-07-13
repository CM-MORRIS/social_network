import React, { useState, useEffect, useLayoutEffect } from "react";
import axiosInstance from "../axiosApi";
import UserPost from "./UserPost";
import { Redirect } from "react-router-dom";
import { makeStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';
import { deepOrange, deepPurple } from '@material-ui/core/colors';
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import Divider from "@material-ui/core/Divider";
import Grid from "@material-ui/core/Grid";
import Button from '@material-ui/core/Button';
import Container from "@material-ui/core/Container"




const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    "& > *": {
      margin: theme.spacing(1),
    },
  },
  orange: {
    color: theme.palette.getContrastText(deepOrange[500]),
    backgroundColor: deepOrange[500],
  },
  purple: {
    color: theme.palette.getContrastText(deepPurple[500]),
    backgroundColor: deepPurple[500],
    width: theme.spacing(10),
    height: theme.spacing(10),
  },
  divider: {
    margin: theme.spacing(3, 0, 3),
  },
}));

export default function Profile(props) {

  const classes = useStyles();

  const username = props.match.params.username;

  const [isRedirect, setRedirect] = useState(false);
  const [isUserValid, setIsUserValid] = useState(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [userPosts, setUserPosts] = useState([]);
  const [isUsersOwnProfile, setIsUsersOwnProfile] = useState(null);
  const [isFollowing, setIsFollowing] = useState(null);
  const [followers, setFollowers] = useState(0);
  const [following, setFollowing] = useState(0);
  
  // /* 
  //   Passing an empty array as the second argument to useEffect 
  //   makes it only run on mount and unmount, thus stopping any infinite loops.
  // */
  // useEffect(() => {
  //   updateFollows();
  // }, [followers, following]); // Only re-run the effect if followers/following changes

  useEffect(() => {
    if (isUserValid == null) {
      validateUser();
    }

    if (isUserValid == false) {
      console.log("user not valid");
      setRedirect(true);
    }

    if (isUserValid == true) {

      getProfile();
      getUserPosts();
      isUsersOwnProfileCheck();
      isFollowingCheck();
      updateFollows();
    }

  }, [isUserValid, followers, following, isFollowing, isUsersOwnProfile]);

  if (isRedirect) {
    return <Redirect to="/home"/>;
  }

  const validateUser = async () => {
    const response = await axiosInstance.get(`/user_exists/${username}`);

    return setIsUserValid(response.data.exists);
  };

  const getProfile = async () => {
    const userDetailsResponse = await axiosInstance.get(`user/${username}`);
    setFirstName(userDetailsResponse.data["first_name"]);
    setLastName(userDetailsResponse.data["last_name"]);
  };

  const getUserPosts = async () => {
    const response = await axiosInstance.get(`user_posts/${username}`);

    setUserPosts(
      response.data.map((post) => ({
        postId: post.pk,
        userId: post.user_id,
        username: post.username,
        text: post.text,
        dateTime: post.date_time,
        likes: post.number_of_likes,
      }))
    );
  };

  const updateFollows = async () => {

    const followersResponse = await axiosInstance.get(`user_followers/${username}`);
    setFollowers(followersResponse.data.followersCount);
  
    const followingResponse = await axiosInstance.get(`user_following/${username}`);
    setFollowing(followingResponse.data.followingCount);

};

  const isUsersOwnProfileCheck = async () => {

    let response = await axiosInstance.get(`get_logged_in_user/`)
    setIsUsersOwnProfile(username === response.data.user_logged_in ? true : false);

  }

  const isFollowingCheck = async () => {

      let response = await axiosInstance.get(`is_following/${username}`)

      setIsFollowing(response.data.isFollowing);
  }

  const follow = async () => {

    const responseFollow = await axiosInstance.post(`follow/${username}`)
    console.log("follow click message: " + responseFollow.data.message)

    const response = await axiosInstance.get(`get_logged_in_user/`)
    setIsUsersOwnProfile(username === response.data.user_logged_in ? true : false);

    const followersResponse = await axiosInstance.get(`user_followers/${username}`);
    setFollowers(followersResponse.data.followersCount);
  
    const followingResponse = await axiosInstance.get(`user_following/${username}`);
    setFollowing(followingResponse.data.followingCount);

  }

  const FollowButton = () => {
    return (
      <div>
        <Button variant="contained" color="primary" onClick={() => follow()}>
          Follow
        </Button>
      </div>
    );
  };

  const UnfollowButton = () => {
    return (

      <div>
        <Button variant="outlined" color="primary" onClick={() => follow()}>
          Unfollow
        </Button>
      </div>
    );
  };
  
  const FollowOrUnfollowButton = () => {

    if(isUsersOwnProfile) {
      return (<div></div>);
    }
    if (isFollowing) {
      return <UnfollowButton/>;
    } else {
      return <FollowButton/>;
    }
  };


  return (
    <div>
    <Container>
      <Box m={1} />

      <Divider light className={classes.divider} />

      <Grid container direction="column" justify="centre" alignItems="center" spacing={2}>
        <div className={classes.root}>
          <Avatar className={classes.purple}>
            <Typography variant="h4">
              {firstName.charAt(0) + lastName.charAt(0)}
            </Typography>
          </Avatar>
        </div>

        <Grid item xs={2}>
          <Typography variant="h6">
            <Box fontWeight="fontWeightBold">{username}</Box>
          </Typography>
        </Grid>

        <Grid item xs={12}>
          <FollowOrUnfollowButton />
        </Grid>
      </Grid>

      <Grid container direction="column">
      <Grid item xs={2} />
      </Grid>

      <Grid container>
        <Grid item xs={2} />
        <Grid item container xs={4} align="center" justify="center">
          <Grid item>Followers</Grid>
        </Grid>
        <Grid item container xs={4} align="center" justify="center">
          <Grid item>Following</Grid>
        </Grid>
        <Grid item xs={2} />
      </Grid>

      <Grid container>
        <Grid item xs={2} />
        <Grid item container xs={4} align="center" justify="center">
          <Grid item>{followers}</Grid>
        </Grid>
        <Grid item container xs={4} align="center" justify="center">
          <Grid item>{following}</Grid>
        </Grid>
        <Grid item xs={2} />
      </Grid>

      <Divider light className={classes.divider} />

      <Grid container direction="column" justify="centre" alignItems="center" spacing={2}>
        <Grid item xs={12}>
          <Typography variant="h5">
            <Box fontWeight="fontWeightBold"> Your posts </Box>
          </Typography>
        </Grid>      
      </Grid>

      {userPosts.map((post) => (
        <div key={post.pk}>
          <UserPost
            postId={post.postId}
            userId={post.userId}
            username={post.username}
            text={post.text}
            dateTime={post.dateTime}
            likes={post.likes}
          />
        </div>
      ))}
  </Container>
    </div>
  );
}
