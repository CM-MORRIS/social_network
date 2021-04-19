import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import axiosInstance from "../axiosApi";
import moment from "moment";

import FavoriteBorderIcon from "@material-ui/icons/FavoriteBorder";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import FavoriteIcon from "@material-ui/icons/Favorite";
import Divider from "@material-ui/core/Divider";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import grey from "@material-ui/core/colors/grey";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    paddingTop: 12,
    paddingBottom: 12,
  },
  paper: {
    padding: theme.spacing(2),
    margin: "auto",
    maxWidth: 500,
    //   backgroundColor: grey[800]
  },
  divider: {
    margin: theme.spacing(1, 0, 0),
  },
  username: {
    color: grey[900],
  },
}));

export default function UserPost(props) {
  const classes = useStyles();

  const postId = props.postId;
  const username = props.username;
  const text = props.text;
  const dateTime = moment(props.dateTime).format("LLL");

  const [likes, setLikes] = useState(props.likes);
  const [isPostLikedByLoggedInUser, setIsPostLikedByLoggedInUser] = useState(
    null
  );

  useEffect(() => {
    getIsPostLikedByLoggedInUser();
  });

  const getIsPostLikedByLoggedInUser = async () => {
    const response = await axiosInstance.get(`/does_like_post/${postId}`);

    setIsPostLikedByLoggedInUser(response.data["is_liked"]);
  };

  const likePost = async () => {
    try {
      let response = await axiosInstance.put(`like_post/${postId}`);

      setLikes(response.data.like_count);
    } catch (error) {
      console.log(error.stack);
    }
  };

  const LikeButton = () => {
    if (isPostLikedByLoggedInUser === "true") {
      return <FavoriteIcon color="action" />;
    } else {
      return <FavoriteBorderIcon />;
    }
  };

  return (
    <div className={classes.root}>
      <Paper className={classes.paper}>
        <Grid item xs={12} sm container direction="column" spacing={1}>
          <Grid
            item
            container
            direction="row"
            justify="space-between"
            alignItems="center"
          >
            <Typography
              component={Link}
              to={`/profile/${username}`}
              variant="h6"
              className={classes.username}
            >
              <Box fontWeight="fontWeightBold">{username}</Box>
            </Typography>
            <Typography variant="subtitle1">{dateTime}</Typography>
          </Grid>

          <Grid
            item
            container
            direction="row"
            justify="flex-start"
            alignItems="center"
          >
            <Typography variant="subtitle1">{text}</Typography>
          </Grid>

          <Divider light className={classes.divider} />

          <Grid
            item
            container
            direction="row"
            justify="flex-start"
            alignItems="center"
          >
            <IconButton aria-label="like post" onClick={() => likePost()}>
              <LikeButton />
            </IconButton>
            <Typography variant="subtitle1">{likes}</Typography>
          </Grid>
        </Grid>
      </Paper>
    </div>
  );
}
