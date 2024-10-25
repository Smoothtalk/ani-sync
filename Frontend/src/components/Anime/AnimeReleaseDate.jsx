import React from "react";
import styles from "../css/anime/animereleasedate.module.css";

export default function AnimeReleaseDate({ release_date }) {
  function cleanupDate(release_date) {
    // get the timezone from the browser
    // convert to correct time with date prettfying
  }

  return (
    <div className={styles.releasedateDiv}>
      <p className={styles.releasedate}>{release_date}</p>
    </div>
  );
}
