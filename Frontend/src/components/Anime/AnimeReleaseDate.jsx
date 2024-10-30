import React from "react";
import styles from "../css/anime/animereleasedate.module.css";

export default function AnimeReleaseDate({ release_date }) {
  function cleanupDate(release_date) {
    // get the timezone from the browser
    // convert to correct time with date prettfying
    return release_date.split(" - ");
  }
  let only_release_date = cleanupDate(release_date)[0];
  let release_time = cleanupDate(release_date)[1];
  return (
    <div className={styles.releasedateDiv}>
      <p className={styles.releasedate}>{only_release_date}</p>
      <p className={styles.releasedate}>{release_time}</p>
    </div>
  );
}
