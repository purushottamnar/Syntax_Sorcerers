import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'model.dart';

class MovieDetailsScreen extends StatelessWidget {
  // Holds the movie data passed from the previous screen
  final MoviesModel movie;

  const MovieDetailsScreen({super.key, required this.movie});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        // Displays the movie title in the app bar
        title: Text(movie.title ?? ''),
        centerTitle: true,
        titleTextStyle: GoogleFonts.poppins(
          fontSize: 20,
          fontWeight: FontWeight.w600,
          color: Colors.white,
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Movie Poster and Basic Info
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Movie Poster
                ClipRRect(
                  borderRadius: BorderRadius.circular(8.0),
                  child: Image.network(
                    movie.poster ?? '',
                    height: 200,
                    width: 140,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) => const Icon(
                        Icons.error,
                        color: Colors.white70,
                        size: 50),
                  ),
                ),
                const SizedBox(width: 16),
                // Basic Movie Info
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Movie title
                      Text(
                        movie.title ?? '',
                        style: GoogleFonts.poppins(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          const Icon(Icons.star, color: Colors.amber, size: 20),
                          const SizedBox(width: 4),
                          Text(
                            '${movie.rating}/10',
                            style: GoogleFonts.poppins(
                              fontSize: 16,
                              color: Colors.amber,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Row(
                        children: [
                          const Icon(Icons.calendar_today,
                              color: Colors.white70, size: 16),
                          const SizedBox(width: 4),
                          Text(
                            '${movie.year}',
                            style: GoogleFonts.poppins(
                              color: Colors.white70,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Row(
                        children: [
                          const Icon(Icons.timer,
                              color: Colors.white70, size: 16),
                          const SizedBox(width: 4),
                          Text(
                            '${movie.runtime} minutes',
                            style: GoogleFonts.poppins(
                              color: Colors.white70,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Genre Section
            _buildSectionTitle('Genre', Icons.movie),
            Wrap(
              spacing: 8,
              children: [
                ...(movie.genre ?? []).map(
                  (genre) => Chip(
                    label: Text(genre),
                    backgroundColor: Colors.blueGrey[700],
                    labelStyle: const TextStyle(color: Colors.white),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Director Section
            _buildSectionTitle('Director', Icons.person),
            Text(
              movie.director ?? '',
              style: GoogleFonts.poppins(
                fontSize: 16,
                color: Colors.white70,
              ),
            ),
            const SizedBox(height: 24),

            // Cast Section
            _buildSectionTitle('Cast', Icons.people),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                ...(movie.actors ?? []).map(
                  (actor) => Chip(
                    avatar: const Icon(Icons.person,
                        color: Colors.white70, size: 16),
                    label: Text(actor),
                    backgroundColor: Colors.blueGrey[700],
                    labelStyle: const TextStyle(color: Colors.white),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Plot Section
            _buildSectionTitle('Plot', Icons.description),
            Text(
              movie.plot ?? '',
              style: GoogleFonts.poppins(
                fontSize: 16,
                color: Colors.white70,
                height: 1.5,
              ),
            ),
            const SizedBox(height: 24),

            // Additional Information
            _buildSectionTitle('Additional Information', Icons.info_outline),
            _buildInfoRow(Icons.emoji_events, 'Awards', movie.awards ?? ''),
            _buildInfoRow(Icons.language, 'Language', movie.language ?? ''),
            _buildInfoRow(Icons.location_on, 'Country', movie.country ?? ''),
            _buildInfoRow(
                Icons.monetization_on, 'Box Office', movie.boxOffice ?? ''),
            _buildInfoRow(Icons.business, 'Production', movie.production ?? ''),
          ],
        ),
      ),
    );
  }

  // Helper method to build section titles
  Widget _buildSectionTitle(String title, IconData icon) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Row(
        children: [
          Icon(icon, color: Colors.white, size: 24),
          const SizedBox(width: 8),
          Text(
            title,
            style: GoogleFonts.poppins(
              fontSize: 20,
              fontWeight: FontWeight.w600,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  // Helper method to build info rows
  Widget _buildInfoRow(IconData icon, String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Colors.white70, size: 16),
          const SizedBox(width: 8),
          Expanded(
            child: RichText(
              text: TextSpan(
                children: [
                  TextSpan(
                    text: '$label: ',
                    style: GoogleFonts.poppins(
                      color: Colors.white,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  TextSpan(
                    text: value,
                    style: GoogleFonts.poppins(
                      color: Colors.white70,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
