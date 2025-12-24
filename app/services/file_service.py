"""
ファイルアップロード処理
"""
import imghdr
import os
from config import Config

class FileService:
    """ファイルアップロードに関するビジネスロジック"""

    def validate_image(self, file):
        """画像ファイルのバリデーション"""
        if not file or not file.filename:
            return None

        # ファイル内容のチェック（マジックナンバー）
        header = file.read(512)
        file_type = imghdr.what(None, header)
        if file_type not in ('jpeg', 'png', 'gif'):
            file.seek(0)
            return '画像ファイルではありません'
        file.seek(0)

        # ファイル形式チェック
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in Config.ALLOWED_EXTENSIONS:
            return 'jpg, jpeg, png, gifのみ対応しています'

        # ファイルサイズチェック
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size > Config.MAX_CONTENT_LENGTH:
            return '画像ファイルは5MB以下にしてください'

        return None

    def save_review_photo(self, file, review_id):
        """レビュー写真を保存"""
        file_ext = os.path.splitext(file.filename)[1].lower()
        filename = f'review_{review_id}{file_ext}'

        # 保存先ディレクトリの確認（存在しなければ作成）
        upload_dir = Config.UPLOAD_FOLDER
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, exist_ok=True)

        # ファイル保存
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        return filename

    def delete_review_photo(self, filename):
        """レビュー写真を削除"""
        if not filename:
            return True

        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                print(f"ファイル削除エラー: {e}")
                return False

        return True
