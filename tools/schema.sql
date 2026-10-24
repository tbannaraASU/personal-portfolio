PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY,
  caption TEXT NOT NULL DEFAULT '',
  title TEXT NOT NULL DEFAULT '',
  published_at TEXT NOT NULL DEFAULT '',
  permalink TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS photos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  position INTEGER NOT NULL,
  path TEXT NOT NULL,
  alt_text TEXT NOT NULL DEFAULT '',
  UNIQUE(post_id, position)
);
CREATE TABLE IF NOT EXISTS hashtags (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tag TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS post_hashtags (
  post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  hashtag_id INTEGER NOT NULL REFERENCES hashtags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, hashtag_id)
);
CREATE INDEX IF NOT EXISTS idx_photos_post ON photos(post_id);
CREATE INDEX IF NOT EXISTS idx_post_hashtags_tag ON post_hashtags(hashtag_id);
CREATE INDEX IF NOT EXISTS idx_posts_published ON posts(published_at DESC);

-- Curated albums are separate from automatic hashtag categories.
-- An album can contain photo sets with any number of different hashtags.
CREATE TABLE IF NOT EXISTS albums (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  cover_post_id TEXT NOT NULL DEFAULT '',
  sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS album_posts (
  album_id TEXT NOT NULL REFERENCES albums(id) ON DELETE CASCADE,
  post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  position INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (album_id, post_id)
);
CREATE INDEX IF NOT EXISTS idx_album_posts_post ON album_posts(post_id);

-- Featured individual images for the homepage, ordered by position. Paths are stable across post metadata edits.
CREATE TABLE IF NOT EXISTS featured_photos (
  photo_path TEXT PRIMARY KEY,
  position INTEGER NOT NULL DEFAULT 0
);
