COMMENT_VERSION = 1.0
POST_VERSION = 1.0
UI_VERSION = 1.0
PROMETHEUS_VERSION = 1.0
USER_NAME = funnyfatty
build: comment_build post_build ui_build prometheus_build
push: comment_push post_push ui_push prometheus_push
comment_build: comment
	docker build -t $(USER_NAME)/comment:$(COMMENT_VERSION) $^
post_build: post-py
	docker build -t $(USER_NAME)/post:$(POST_VERSION) $^
ui_build: ui
	docker build -t $(USER_NAME)/ui:$(UI_VERSION) $^
prometheus_build: prometheus
	docker build -t $(USER_NAME)/prometheus:$(PROMETHEUS_VERSION) $^
comment_push: comment
	docker push $(USER_NAME)/comment:$(COMMENT_VERSION)
post_push: post-py
	docker push $(USER_NAME)/post:$(POST_VERSION)
ui_push: ui
	docker push $(USER_NAME)/ui:$(UI_VERSION)
prometheus_push: prometheus
	docker push $(USER_NAME)/prometheus:$(PROMETHEUS_VERSION)
