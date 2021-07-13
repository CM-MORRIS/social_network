import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosApi";
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import IconButton from "@material-ui/core/IconButton";
import Grid from "@material-ui/core/Grid";

export default function FollowButton(props) {
 

  const userProfile = props.userProfile;

  const [isUsersOwnProfile, setIsUsersOwnProfile] = useState(null);
  const [isFollowing, setIsFollowing] = useState(null);
  const [followers, setFollowers] = useState(0);
  const [following, setFollowing] = useState(0);


  useEffect(() => {

    isUsersOwnProfileCheck();
    isFollowingCheck();
    updateFollows();

  },[isFollowing, followers, following]);

  const updateFollows = async () => {

    const followersResponse = await axiosInstance.get(`user_followers/${userProfile}`);
    setFollowers(followersResponse.data.followersCount);
  
    const followingResponse = await axiosInstance.get(`user_following/${userProfile}`);
    setFollowing(followingResponse.data.followingCount);

};

  const isUsersOwnProfileCheck = async () => {

    let response = await axiosInstance.get(`get_logged_in_user/`)

    setIsUsersOwnProfile(userProfile === response.data.user_logged_in ? true : false);

  }

  const isFollowingCheck = async () => {

      let response = await axiosInstance.get(`is_following/${userProfile}`)

      setIsFollowing(response.data.isFollowing);
  }

  const follow = async () => {

    const response = await axiosInstance.post(`follow/${userProfile}`)
    console.log("follow click message: " + response.data.message)

    updateFollows();

  }

  const Follow = () => {
    return (
      <div>
        <Button variant="outlined" color="primary">
          Follow
        </Button>
      </div>
    );
  };

  const Unfollow = () => {
    return (

      <div>
        <Button variant="outlined" color="primary">
          Unfollow
        </Button>
      </div>
    );
  };
  
  const Button = () => {

    if(isUsersOwnProfile) {
      return (<div></div>);
    }

    if (isFollowing) {
      return <Unfollow/>;
    } else {
      return <Follow/>;
    }
  };

  const useStyles = makeStyles((theme) => ({
    root: {
      "& > *": {
        margin: theme.spacing(1),
      },
    },
  }));

  const classes = useStyles();

  return (
    <div className={classes.root}>
      <Grid container direction="row" justify="center" alignItems="center">
        <Button onClick={() => follow()} />
      </Grid>

      <Grid container direction="row" justify="center" alignItems="center">
        <Grid item xs={2}>
          Followers
        </Grid>

        <Grid item xs={1}>
          Following
        </Grid>
      </Grid>

      <Grid container direction="row" justify="center" alignItems="centre">
        <Grid item xs={2}>
          {followers}
        </Grid>

        <Grid item xs={1}>
          {following}
        </Grid>
      </Grid>
    </div>
  );

}

