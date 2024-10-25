import React from "react";
import AnimeTitle from "./AnimeTitle";
import AnimeEpisodeNum from "./AnimeEpisodeNum";
import AnimeIcon from "./AnimeIcon";
import AnimeReleaseDate from "./AnimeReleaseDate";

import styles from "../css/anime/animeentry.module.css";

export default function AnimeEntry({ anime }) {
  return (
    <div className={styles.entry}>
      <AnimeIcon anime_id={anime.anime} />
      <AnimeTitle title={anime.release_title} />
      <AnimeEpisodeNum episode={anime.episode_num} />
      <AnimeReleaseDate release_date={anime.pub_date} />
    </div>
  );
}
