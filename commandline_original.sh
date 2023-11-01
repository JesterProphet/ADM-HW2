jq '{id: .id, title: .title, worksLength: (.works | length)}' series.json > series_with_books_count.json
jq -s 'sort_by(.worksLength) | reverse |  .[:5]' series_with_books_count.json > sorted_series_with_books_count.json
jq -r '["id", "title", "total_books_count"], (.[] | [.id, .title, .worksLength]) | @tsv' sorted_series_with_books_count.json | column -t -s $'\t'