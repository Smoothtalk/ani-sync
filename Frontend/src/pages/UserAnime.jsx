import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../context/UserContext"; // Correct context import
import ClipLoader from "react-spinners/ClipLoader";
import style from "../components/css/useranime/useranime.module.css";
import AnimeIcon from "../components/Anime/AnimeIcon"; // Custom component

export default function UserAnime() {
  const { user, loading } = useContext(UserContext); // Get user from context
  const URL = "/anilist/get_user_anime/?username=";
  const [animeList, setAnimeList] = useState([]);
  const [selectedAnime, setSelectedAnime] = useState(null);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    // Fetch user anime from your Django backend
    fetch(`${URL}${user.username}`)
      .then(res => res.json())
      .then(data => {
        setAnimeList(data);
        setIsFetching(false);
      })
      .catch(err => console.error("Error fetching anime:", err));
  }, []);

  // Show a loader if the user or anime list is still loading
  if (loading || isFetching) {
    return <ClipLoader color="#ffffff" loading={true} size={50} />;
  }

  function getAnimeIconURL(show_id) {
    const URL = "/anilist/get_anime_icon/?anime_id="

    fetch(`${URL}${show_id}`)
      .then(data => {
        return data.text()
      })
      .then(url => {
        setSelectedAnime(prev => ({ 
            ...prev, 
            icon_url: url 
        }));
      })
      .catch(err => console.error("Error fetching anime icon:", err));
  }


  return (
    <div className={style.container}>
      <h1 className={style.welcome_message}>Welcome, {user?.username}</h1>
      
      <select 
        className={style.selectBox}
        onChange={(e) => {
            const anime = animeList.find(a => a.show_id.toString() === e.target.value);
            setSelectedAnime(anime);
            getAnimeIconURL(anime.show_id)
        }}
      >
        <option value="">Select an Anime</option>
        {animeList.map(anime => (
          <option key={anime.show_id} value={anime.show_id}>{anime.anime_title}</option>
        ))}
      </select>

      {selectedAnime && (
        <div className={style.details}>
          {/* Using your custom AnimeIcon component */}
          <AnimeIcon icon_url={selectedAnime.icon_url} anime_id={selectedAnime.show_id} />
          <p className={style.anime_title}>{selectedAnime.anime_title}</p>
        </div>
      )}
    </div>
  );
}