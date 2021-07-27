#include <cstddef>
#include <algorithm>
#include <iostream>

template <class T>
class SharedPtr {
    T *elem_;
    int *cnt_;

    void sub() {
        if (cnt_ && !--*cnt_) {
            delete elem_;
            delete cnt_;
        }
    }

public:
    SharedPtr() : elem_(nullptr), cnt_(nullptr) {}

    SharedPtr(T *elem) : elem_(elem), cnt_(new int{1}) {}

    SharedPtr(const SharedPtr<T>& other) noexcept {
        elem_ = other.elem_;
        cnt_ = other.cnt_;
        if (cnt_) {
            ++*cnt_;
        }
    }

    SharedPtr(SharedPtr<T>&& other) noexcept {
        elem_ = std::move(other.elem_);
        cnt_ = std::move(other.cnt_);
        other.elem_ = nullptr;
        other.cnt_ = nullptr;
    }

    SharedPtr<T>& operator=(T *elem) noexcept {
        sub();
        elem_ = elem;
        cnt_ = new int{1};
        return *this;
    }

    SharedPtr<T>& operator=(const SharedPtr<T>& other) noexcept {
        if (get() == other.get()) {
            return *this;
        }
        sub();
        elem_ = other.elem_;
        cnt_ = other.cnt_;
        if (cnt_) {
            ++*cnt_;
        }
        return *this;
    }

    SharedPtr<T>& operator=(SharedPtr<T>&& other) noexcept {
        if (get() == other.get()) {
            return *this;
        }
        sub();
        elem_ = std::move(other.elem_);
        cnt_ = std::move(other.cnt_);
        other.elem_ = nullptr;
        other.cnt_ = nullptr;
        return *this;
    }

    const T& operator*() const noexcept {
        return *elem_;
    }

    T& operator*() noexcept {
        return *elem_;
    }

    T* operator->() const noexcept {
        return elem_;
    }

    void reset(T *ptr) noexcept {
        SharedPtr<T>(ptr).swap(*this);
    }

    void swap(SharedPtr<T>& other) noexcept {
        std::swap(elem_, other.elem_);
        std::swap(cnt_, other.cnt_);
    }

    void swap(SharedPtr<T>& l, SharedPtr<T>& r) noexcept {
        std::swap(l.elem_, r.elem_);
        std::swap(l.cnt_, r.cnt_);
    }

    T* get() const {
        return elem_;
    }

    explicit operator bool() const {
        return elem_ != nullptr;
    }

    ~SharedPtr() {
        sub();
    }
};
