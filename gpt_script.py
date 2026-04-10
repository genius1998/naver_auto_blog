from publisher_core import NaverBlogPublisher, PublishConfig


def post_to_naver_blog(keyword="최신 기술", log=print):
    publisher = NaverBlogPublisher(PublishConfig.from_env())
    return publisher.publish(keyword, log=log)


if __name__ == "__main__":
    post_to_naver_blog()
