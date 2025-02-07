from database import insert_data, fetch_data, update_data, delete_data

insert_data("collections", {
    "collection": "test-collection",
    "name": "Test NFT",
    "description": "This is a test NFT collection",
    "image_url": "https://test.com/image.png",
    "owner": "0x123456789abcdef",
    "twitter_username": "test_user",
    "contracts": "0xabcdef123456"
})

print("All Data:", fetch_data("collections"))

print("Filtered Data:", fetch_data("collections", filters={"owner": "0x123456789abcdef"}))

update_data("collections", filters={"collection": "test-collection"}, new_values={"name": "Updated NFT Name"})
print("Updated Data:", fetch_data("collections", filters={"collection": "test-collection"}))

delete_data("collections", filters={"collection": "test-collection"})
print("Deleted Data:", fetch_data("collections"))