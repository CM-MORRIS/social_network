import React, { useState, useEffect } from "react";
import axiosInstance from "../axiosApi";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";
import Button from '@material-ui/core/Button';
import Container from "@material-ui/core/Container"
import SendIcon from '@material-ui/icons/Send';
import Box from "@material-ui/core/Box";


const useStyles = makeStyles((theme) => ({

  root: {
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
      width: "50ch",
    },
    button: {
        margin: theme.spacing(1),
    },
    divider: {
        margin: theme.spacing(3, 0, 3),
    },
  },
}));

const constants = {
  MIN_CHARACTERS: 1,
  MAX_CHARACTERS: 280,
};

export default function CreatePost() {

  const classes = useStyles();
  const [postText, setPostText] = useState("");

  useEffect(() => {}, []);

  const handleSubmit = async () => {
    alert("try submit");

    // is valid submission
    if (postText.length >= constants.MIN_CHARACTERS &&
        postText.length <= constants.MAX_CHARACTERS) {

      const response = await axiosInstance.post("create_post/", {
        text: postText,
      });

      // empty text input after submit
      setPostText("");
    } else {
      alert("invalid submission");
    }
  };

  const updatePostText = (event) => {
    setPostText(event.target.value);
  };


  return (
    <div>
      <Container>
        <Box m={5} />

        <Grid
          container
          direction="column"
          justify="centre"
          alignItems="center"
          spacing={2}
        >
          <form className={classes.root} noValidate autoComplete="off">
            <TextField
              id="outlined-multiline-static"
              label="What's on your mind..."
              multiline
              rows={6}
              variant="outlined"
              value={postText}
              onChange={updatePostText}
              helperText={postText.length + "/" + constants.MAX_CHARACTERS}
            />
          </form>

          <Button
            variant="contained"
            color="primary"
            className={classes.button}
            endIcon={<SendIcon />}
            onClick={() => handleSubmit()}
          >
            Post
          </Button>
        </Grid>
      </Container>
    </div>
  );
}
