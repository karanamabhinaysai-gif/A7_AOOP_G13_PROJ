package com.bookmyshow.catalog;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * U7: Catalog Context - Service to search movies and cinemas
 */
public class CatalogService {
    private final Map<String, Movie> movies = new ConcurrentHashMap<>();
    private final Map<String, Cinema> cinemas = new ConcurrentHashMap<>();

    public void addMovie(Movie movie) {
        movies.put(movie.movieId(), movie);
    }

    public void addCinema(Cinema cinema) {
        cinemas.put(cinema.cinemaId(), cinema);
    }

    public Optional<Movie> findMovieById(String movieId) {
        return Optional.ofNullable(movies.get(movieId));
    }

    public Optional<Cinema> findCinemaById(String cinemaId) {
        return Optional.ofNullable(cinemas.get(cinemaId));
    }

    public List<Movie> listMovies() {
        return List.copyOf(movies.values());
    }

    public List<Cinema> listCinemasInCity(String city) {
        return cinemas.values().stream()
                .filter(c -> c.city().equalsIgnoreCase(city))
                .toList();
    }
}
