import React, { useEffect, useState } from "react";
import styles from "../css/anime/animeicon.module.css";

export default function AnimeIcon({ icon_url }) {
  return (
    <div className={styles.animeIconDiv}>
      <img className={styles.animeIcon} src={icon_url} />
    </div>
  );
}
