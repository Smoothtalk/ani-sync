import React from "react";
import AnimeTitle from "./AnimeTitle";
import AnimeIcon from "./AnimeIcon";
import AnimeReleaseDate from "./AnimeReleaseDate";

import styles from "../css/anime/animeentry.module.css";
import AnimeEpisodeNum from "./AnimeEpisodeNum";

export default function AnimeEntry({ anime }) {
  return (
    <div className={styles.entry}>
      <AnimeIcon icon_url={anime.icon_url} anime_id={anime.anime} />
      <AnimeTitle title={anime.simple_title} anime_id={anime.anime} />
      <AnimeEpisodeNum episode={anime.episode_num} />
      <AnimeReleaseDate release_date={anime.pub_date} />
    </div>
  );
}
